import random


def alphabet_gen(lt=""):
    from string import letters
    all_l = letters
    if lt:
        all_l = letters.replace(lt, "")
        letter = random.choice(all_l)
    else:
        letter = random.choice(all_l)
    return letter


def change(word):
    original = word
    word = list(word)
    methods = ["replace", "remove", "insert"]
    choice = random.choice(methods)

    if len(word) < 4:
        how_many = 1
        choice = random.choice(["replace", "insert"])
    else:
        how_many = random.choice(range(1, 3))

    if choice == "replace":
        indexes = random.sample(range(len(word)), how_many)
        for index in indexes:
            lt = word[index]
            word[index] = alphabet_gen(lt)
    elif choice == "remove":
        for i in xrange(how_many):
            index = random.choice(range(len(word)))
            del word[index]
    else:
        for i in xrange(how_many):
            word.append(alphabet_gen())
    word = "".join(word)
    return word
