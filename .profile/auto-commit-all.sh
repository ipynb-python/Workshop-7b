#!/bin/bash

# Ensure bash environment is sourced for user settings like PATH
source ~/.bashrc

# --- Configuration ---
BASE_DIR="/workspaces"
SLEEP_INTERVAL=10
SHADOW_BASE_DIR="/tmp/autosave-shadows"

# --- Branch Names ---
MAIN_BRANCH_NAME="main"
AUTOSAVE_BRANCH_NAME="autosave"

# --- Lock Configuration ---
# Lock for the single, master launcher process
LAUNCHER_LOCKFILE="/tmp/auto-commit-launcher.lock"
# Lock prefix for individual repository watcher processes
WATCHER_LOCK_PREFIX="/tmp/auto-commit-lock-"

# --- Verbose Flag Setup ---
VERBOSE=0
# Process -v flag first
if [ "$1" == "-v" ]; then
    VERBOSE=1
    shift # Remove the -v flag from the arguments list
fi

# Custom echo function: prints only if VERBOSE=1
vecho() {
    if [ "$VERBOSE" -eq 1 ]; then
        echo "$@"
    fi
}
# -----------------------------

# --- Script Logic ---

# --- Halt Flag Check (-h) ---
# This is the ONLY way to deliberately stop running watchers.
if [ "$1" == "-h" ]; then
    echo "Halt flag detected. Stopping all running watcher processes..."
    # Find all PIDs running this script, excluding the current PID
    EXISTING_PIDS=$(pgrep -f "$0" | grep -v $$)
    
    if [ -n "$EXISTING_PIDS" ]; then
        for PID in $EXISTING_PIDS; do
            echo " - Stopping (PID: $PID)..."
            # Send TERM signal to allow graceful lock release (trap in WATCHER MODE)
            kill "$PID"
        done
        echo "All watcher processes halted."
    else
        echo "No running watcher processes found."
    fi

    # Clean up the launcher lock file, just in case
    rm -f "$LAUNCHER_LOCKFILE"
    
    # Inform about potential stale locks
    echo "---"
    echo "If you encounter 'Watcher is already running' errors after this, a process"
    echo "may have died unexpectedly leaving a stale lock. You may need to manually"
    echo "delete stale lock files using: rm -f ${WATCHER_LOCK_PREFIX}*.lock"
    echo "---"
    exit 0
fi


if [ $# -eq 0 ]; then
    ### LAUNCHER MODE ###
    
    # --- LAUNCHER LOCK ACQUISITION ---
    exec 201>"$LAUNCHER_LOCKFILE"
    
    # Try to acquire the lock without blocking (-n)
    flock -n 201 || {
        echo "Launcher already running (PID: $(cat "$LAUNCHER_LOCKFILE")). Exiting new instance." >&2
        exec 201>&- # Release file descriptor
        exit 1
    }
    
    # If lock acquired, set trap to release it on exit
    trap 'vecho "Launcher (PID: $$) finished and releasing lock."; exec 201>&-; exit 0' EXIT SIGINT SIGTERM
    vecho "Launcher Mode (PID: $$): Lock acquired. Starting scan..."
    # --- END LAUNCHER LOCK ---
    
    SCRIPT_PATH=$(realpath "$0")
    
    vecho "Finding all git repos under $BASE_DIR..."
    
    if [ ! -f "$SCRIPT_PATH" ]; then
        echo "Error: Could not determine script's full path. Is 'realpath' installed?" >&2
        exec 201>&-
        exit 1
    fi
    
    # Iterate over every git repository found
    find "$BASE_DIR" -type d -name ".git" | while read GIT_DIR; do
        REPO_DIR=$(dirname "$GIT_DIR")
        vecho " - Found repo: $REPO_DIR"
        
        # Pass the -v flag if the launcher was started with -v to the new watcher process
        VERBOSE_FLAG=""
        if [ "$VERBOSE" -eq 1 ]; then
            VERBOSE_FLAG="-v"
            LOG_NAME=$(echo "$REPO_DIR" | tr '/' '_' | sed 's/^_//')
            LOG_FILE="/tmp/auto-commit-$LOG_NAME.log"
            vecho "   -> Attempting to start new watcher. Log file: $LOG_FILE"
            nohup "$SCRIPT_PATH" $VERBOSE_FLAG "$REPO_DIR" > "$LOG_FILE" 2>&1 &
        else
            # If not verbose, redirect output to null
            nohup "$SCRIPT_PATH" $VERBOSE_FLAG "$REPO_DIR" > /dev/null 2>&1 & 
        fi
        
    done
    
    vecho "Launcher finished. New watcher processes are starting."
    vecho "Use '$0 -h' to stop all watchers."
    # The trap EXIT handles releasing the launcher lock here.
    
else
    ### WATCHER MODE ###
    # NOTE: $1 is now guaranteed to be the TARGET_DIR because the -v flag was shifted
    TARGET_DIR="$1"
    
    # --- 1. Set up Lock (Watcher Lock) ---
    LOCK_NAME=$(echo "$TARGET_DIR" | tr -c 'a-zA-Z0-9' '_')
    LOCKFILE="${WATCHER_LOCK_PREFIX}$LOCK_NAME.lock"

    # Open file descriptor 200 for the lock file
    exec 200>"$LOCKFILE"
    
    # Try to acquire the lock non-blockingly
    flock -n 200 || {
        # Fails if another watcher for this repo is already running
        echo "[$TARGET_DIR] Error: Watcher is already running (PID: $(cat "$LOCKFILE" 2>/dev/null)). Exiting." >&2
        exec 200>&- 
        exit 1
    }
    
    # Set trap to release the lock on graceful exit (SIGINT/SIGTERM)
    trap 'vecho "[$TARGET_DIR] Watcher (PID: $$) stopping and releasing lock."; exec 200>&-; exit 0' SIGINT SIGTERM
    
    vecho "[$TARGET_DIR] Watcher starting (PID: $$). Lock acquired."
    
    # --- Check if on Main Branch ---
    CURRENT_BRANCH=$(git -C "$TARGET_DIR" rev-parse --abbrev-ref HEAD)
    if [ "$CURRENT_BRANCH" != "$MAIN_BRANCH_NAME" ]; then
        echo "[$TARGET_DIR] Error: Watcher stopped. You are on branch '$CURRENT_BRANCH'." >&2
        echo "[$TARGET_DIR] Autosave only works when you are on '$MAIN_BRANCH_NAME'." >&2
        exec 200>&- # Release lock
        exit 1
    fi
    vecho "[$TARGET_DIR] Verified you are on '$MAIN_BRANCH_NAME'. Proceeding."

    # --- 2. Set up Shadow Repo ---
    SHADOW_DIR="$SHADOW_BASE_DIR/$LOCK_NAME"
    mkdir -p "$SHADOW_BASE_DIR"
    
    vecho "[$TARGET_DIR] Creating fresh shadow repo at: $SHADOW_DIR"
    rm -rf "$SHADOW_DIR"
    
    git clone "$TARGET_DIR" "$SHADOW_DIR" || { echo "[$TARGET_DIR] Error: Clone failed. Exiting." >&2; exec 200>&-; exit 1; }
    cd "$SHADOW_DIR" || { echo "[$TARGET_DIR] Error: cd to shadow failed. Exiting." >&2; exec 200>&-; exit 1; }
    
    # --- 3. Configure Remote and Branch ---
    vecho "[$TARGET_DIR] Setting remote URL..."
    REAL_ORIGIN_URL=$(git -C "$TARGET_DIR" remote get-url origin)
    git remote set-url origin "$REAL_ORIGIN_URL"
    git config push.autoSetupRemote true
    
    vecho "[$TARGET_DIR] Checking for existing branch $AUTOSAVE_BRANCH_NAME..."
    git fetch origin
    
    if git show-ref --verify --quiet "refs/remotes/origin/$AUTOSAVE_BRANCH_NAME"; then
        vecho "[$TARGET_DIR]   -> Found remote branch. Resuming history."
        git checkout "$AUTOSAVE_BRANCH_NAME"
    else
        vecho "[$TARGET_DIR]   -> No remote branch found. Creating new one."
        git checkout -b "$AUTOSAVE_BRANCH_NAME"
        
        # Add the warning file on the very first commit
        echo "WARNING: This is an automated branch. Do not work here. Your changes will be overwritten." > WARNING.txt
        git add WARNING.txt
        git commit -m "Init autosave and add WARNING.txt"
        git push origin "$AUTOSAVE_BRANCH_NAME"
    fi
    
    # --- 4. Main Watcher Loop ---
    vecho "[$TARGET_DIR] Starting watch loop on $AUTOSAVE_BRANCH_NAME..."
    while true
    do
        # --- A. Sync with Remote (Overwrite conflicts) ---
        git fetch origin
        git reset --hard "origin/$AUTOSAVE_BRANCH_NAME"
        
        # --- B. Copy Changes (rsync) ---
        # Exclude .git directory to prevent conflict
        rsync -a --delete --exclude=".git" "$TARGET_DIR/" "$SHADOW_DIR/"
        
        # --- C. Ensure Warning File Exists ---
        echo "WARNING: This is an automated branch. Do not work here. Your changes will be overwritten." > WARNING.txt
        
        # --- D. Commit and Push ---
        git add .
        
        if [ -n "$(git status --porcelain)" ]; then
            vecho "[$TARGET_DIR] Changes detected at $(date +'%Ym%d-%H%M%S'). Committing..."
            
            git commit -m "auto-commit: $(date +'%Ym%d-%H%M%S')"
            
            vecho "[$TARGET_DIR] Pushing to $AUTOSAVE_BRANCH_NAME..."
            
            # Standard (non-force) push. Will fail if remote has new commits.
            git push origin "$AUTOSAVE_BRANCH_NAME" || {
                echo "[$TARGET_DIR] WARNING: Push failed. Will attempt to sync and re-commit next cycle." >&2
            }
            
            vecho "[$TARGET_DIR] Push complete. Waiting..."
        fi
        
        sleep $SLEEP_INTERVAL
    done
fi