import random


def roll_dice(dice):
    """

    :param dice: String of what dice to roll and how many, plus modifier of the form: "1d4+2"
    :return: String representing each individual dice and their sum
    """
    modifier = 0

    # Parse the dice
    no_spaces = "".join(dice.split())

    # check for modifier
    if "+" in no_spaces:
        modifier = no_spaces.split("+")[-1]
        no_mod = no_spaces[:-2]
    else:
        no_mod = no_spaces

    splits = no_mod.split("d")
    num_dice = int(splits[0])
    die = int(splits[1])

    rolls = []
    total = 0
    for roll in range(num_dice):
        face = random.randint(1, die)
        total += face
        rolls.append(str(face))

    total += int(modifier)

    results = " + ".join(rolls)
    results = f"{results} + {modifier} = {total}"
    return results
