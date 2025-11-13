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
    vecho "Launcher Mode (PID: $$): Lock acquired. Starting scan