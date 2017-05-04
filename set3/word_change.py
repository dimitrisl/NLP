import random


def alphabet_gen():
    from string import letters
    letter = random.choice(letters)
    return letter


def change(word):
    methods = ["replace", "remove", "insert"]
    choice = random.choice(methods)
    how_many = random.choice(range(1, len(word)-1))
    word = list(word)
    if choice == "replace":
        for times in range(how_many):
            index = random.choice(range(len(word)))
            word[index] = alphabet_gen()
    elif choice == "remove":
        for times in range(how_many):
            index = random.choice(range(len(word)))
            del word[index]
    else:
        word.append(alphabet_gen())
    word = "".join(word)
    return word
