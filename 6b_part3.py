def process_str(mystr, mod_dict):
    for key, value in mod_dict.items():
        # you do not need to change the code below
        target = key
        replacement = value
        print(f" ( replacing {target} with {replacement} ) ")
        mystr = mystr.replace(target, replacement)
    return mystr

mod_dict = {"cat": "dog", "red": "blue"}
demo1 = process_str("The cat sat on the red mat.",mod_dict)
print(demo1)