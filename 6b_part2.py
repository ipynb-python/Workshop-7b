def max_length(word1, word2, word3):
    word_list = [ word1, word2, word3 ]   
    # you do not need to change the code below
    longest_word = word_list[0]
    for item in word_list:
        if len(item) > len(longest_word):
            longest_word = item
    return len(longest_word)


demo1 = max_length("cat","beetles","dogs")
print(demo1)