#!/bin/python3
"""
This script reads from a series of tables and assembles an NPC from them.

If you make changes to the default stats dict in render_stats you can balance 
this according to the power of the players that you have.
"""
from random import choice, sample
from itertools import cycle


class NPC:
    """
    A neat object for containing all of an NPC's info. You could easily import this into
    a larger project that needs NPCs!
    """

    def __init__(self, level: int = 1):
        """
        First name uses gender to determine which list of names to use.
        If the gender is other then it randomly picks between male/female names.
        """
        self.level: int = level
        self.gender = read_table("genders")
        self.first_name = first_name_gen(self)
        self.last_name = read_table("family")
        self.race = read_table("race")
        self.job = read_table("jobs")
        self.stats = render_stats(self)

        self.hair = read_table("hair")
        self.eyes = read_table("eyes")
        self.skin = read_table("skin_tone")
        self.quirks = read_table("quirks", 2)
        self.motiv = read_table("motivations")

    def __repr__(self) -> str:
        """
        This allows you to cleanly write the NPC to the console or a file.
        """
        return f"{self.first_name} {self.last_name}, {self.gender}, {self.race}/{self.job}, Lv. {self.level}.\n{self.hair} hair, {self.eyes} eyes, {self.skin} skin.\n{self.stats}\nQuirks: {self.quirks}\nMotivation: {self.motiv}"


def read_table(filename: str, count: int = 1):
    """
    If count is 1 then this grabs a random choice from the given table. Otherwise
    it grabs count choices using random.sample to avoid duplicates.

    That second feature is only used for quirks in this file but it can extended to any DND
    table you can imagine!
    """
    with open(f"tables/{filename}.txt", "r", encoding="UTF-8") as tmpfile:
        lines = [line.strip() for line in tmpfile.readlines()]
    if count == 1:
        return choice(lines)
    else:
        return " ".join(sample(lines, count))


def first_name_gen(C: NPC):
    """
    This handles the other gender object by choosing from the male/female names at random.
    You could absolutely extend this with a third non-binary list of names instead.
    """
    name_gender = C.gender
    if name_gender == "other":
        name_gender = choice(["male", "female"])
    return read_table(name_gender)


def dice(x: int = 20):
    """
    This can be any dice in the game, and can easily be used for hp or attack rolls.
    x defaults to 20 for ease of use but I recommend using real dice for role-play and digital
    dice for mass generation.
    """
    if x < 2:
        print(f"The smallest dice you can roll is two sided but you tried {x}.")
        return 0
    return choice(range(1, x + 1))


def modify(stat: int):
    """
    This takes any stat value and returns it's modifier. You may also do this in your
    head but Python needs the formula.
    """
    return (stat - 10) // 2


def calc_hp(level: int, con: int, hit: int):
    """
    This is the standard DND HP formula per level. This can be used
    to calculate fully legal player character HP stats.

    All you need is the characters level, constitution and hit dice.
    """
    mod = modify(con)
    hp = mod + hit
    if level == 1:
        return hp

    for _ in range(level - 1):
        hp += mod + dice(hit)
    return hp


# C stands for character in this function, I didn't want to confuse it
# with "cha" which stands for charisma.
def render_stats(C: NPC):
    """
    This one function does a lot and holds many internal dicts. But it allows
    us to fully calculate the stats of an NPC at any level with any race/class combo.

    You have to track race/class abilities yourself. Things like dark-vision are not
    documented here but the books should have that info.

    You can modify a lot by simply changing the starting stats dict at the top of the func because
    all the other calculations are additive. You can even set the starting stats to be negative for
    nerfed NPCs.

    The word "hit" refers to the hit dice for a given NPC throughout this function.
    """

    # Base stats, adjust as needed.
    stats: dict = {
        "hp": 3,
        "dc": 11,
        "spd": 5,
        "str": 8,
        "int": 8,
        "dex": 8,
        "wis": 8,
        "con": 8,
        "cha": 8,
        "hit": 0,
    }

    # These are the movement speed and stat values given for each race.
    race_bonuses: dict = {
        "Dragonborn": [("spd", 30), ("str", 2), ("cha", 1)],
        "Dwarf": [("spd", 25), ("con", 2)],
        "Elf": [("spd", 30), ("dex", 2)],
        "Gnome": [("spd", 25), ("int", 2)],
        "Halfling": [("spd", 25), ("dex", 2)],
        "Half-Elf": [("spd", 30), ("cha", 2)],
        "Half-Orc": [("spd", 30), ("str", 2), ("con", 1)],
        "Human": [("spd", 30)],
        "Tiefling": [("spd", 30), ("int", 1), ("cha", 2)],
    }

    # This is six points focused on the given classes preferred stats.
    # This helps the random NPC have a little focus without min-maxing.
    # And it tracks the NPC's hit dice too!
    class_bonuses: dict = {
        "Barbarian": [("con", 4), ("str", 2), ("hit", 12)],
        "Bard": [("cha", 4), ("int", 2), ("hit", 8)],
        "Cleric": [("wis", 4), ("cha", 2), ("hit", 8)],
        "Druid": [("wis", 4), ("dex", 2), ("hit", 8)],
        "Fighter": [("str", 4), ("con", 2), ("hit", 10)],
        "Monk": [("dex", 4), ("wis", 2), ("hit", 8)],
        "Paladin": [("cha", 4), ("str", 2), ("hit", 10)],
        "Ranger": [("str", 4), ("dex", 2), ("hit", 10)],
        "Rogue": [("dex", 4), ("cha", 2), ("hit", 8)],
        "Sorcerer": [("con", 4), ("int", 2), ("hit", 6)],
        "Warlock": [("int", 4), ("con", 2), ("hit", 8)],
        "Wizard": [("int", 4), ("wis", 2), ("hit", 6)],
    }

    # These lines add race bonuses
    race = race_bonuses[C.race]
    for pair in race:
        key, val = pair[0], pair[1]
        stats[key] += val

    # These lines add class bonuses
    cls = class_bonuses[C.job]
    for pair in cls:
        key, val = pair[0], pair[1]
        stats[key] += val

    # The stat pool starts at 21 because the class already spent six points. There is an additional
    # point per level beyond level 1.
    pool: int = 21 + ((C.level - 1) * 1)
    count = 0
    # This cycle just puts one point in each stat until the pool is empty.
    for stat in cycle(["str", "int", "dex", "wis", "con", "cha"]):
        if pool < 1:
            break

        # Tried to stop NPCs from putting too many points into any one stat at level 1.
        if stats[stat] < 18 + C.level // 4:
            stats[stat] += 1
            pool -= 1
        else:
            count += 1

        # This stops infinite looping when all stats are maxed and the pool isn't empty.
        if count > 1000:
            break

    # This is fully DND legal HP.
    stats["hp"] += calc_hp(C.level, stats["con"], stats["hit"])

    # Maybe add the level // 4 or something.
    stats["dc"] += modify(stats["dex"]) + (C.level // 4)

    res = ", ".join([f"{k} {v}" for k, v in stats.items()])
    return res


if __name__ == "__main__":
    # No need for argv if this is being used as a module!
    from sys import argv

    # This cleverly handles the IndexError and the ValueError with the same default value.
    try:
        level = int(argv[1])
    except:
        level = 1

    print(NPC(level))
