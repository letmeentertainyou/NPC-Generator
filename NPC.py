#!/bin/python3
"""
This script reads from a series of tables and assembles an NPC from them.

If you make changes to the default stats dict in generate_stats you can balance 
this according to the power of the players that you have.
"""
from random import choice, sample
from itertools import cycle


class NPC:
    """
    A neat object for containing all of an NPC's info. You could easily import this into
    a larger project that needs NPCs!
    """

    def __init__(self, level: int = 1) -> None:
        """
        Randomly chooses all the traits for the NPC from the include tables.
        """
        self.level: int = level
        self.gender: str = read_table("genders")
        self.first_name: str = read_table(self.gender)
        self.last_name: str = read_table("family")
        self.hair: str = read_table("hair")
        self.eyes: str = read_table("eyes")
        self.skin: str = read_table("skin-tones")
        self.quirks: str = read_table("quirks", 2)
        self.motiv: str = read_table("motivations")
        self.race: str = read_table("race")
        self.job: str = read_table("jobs")
        self.stats: dict = generate_stats(self)

    def __repr__(self) -> str:
        """
        This allows you to cleanly write the NPC to the console or a file. It's unfortunately
        a little sloppy with 12 attributes, I thought about have it print four different lines but
        __repr__ must return a string so it remains until I rethink the API.
        """

        # I just learned this weird string data structure thing!
        _repr: str = (
            f"{self.first_name} {self.last_name}, {self.gender}, {self.race}/{self.job}, "
            f"Lv.{self.level}.\n{self.hair} hair, {self.eyes} eyes, {self.skin} skin."
            f"\n{self.__stat_repr__()}\nQuirks: {self.quirks}\nMotivation: {self.motiv}"
        )
        return _repr

    def __stat_repr__(self) -> str:
        """
        Joins self.stats into a string for console output. This used to be part of the
        generate_stats() function but I moved it out because passing the stats dict
        seems more useful for extending this module.
        """
        res: str = ", ".join([f"{k} {v}" for k, v in self.stats.items()])
        return res


def shuffled(iterable):
    """
    This function is a drop in replacement for random.shuffle() that returns the shuffled iterator
    instead of none. It behaves the same way that sorted() and reversed() do.
    """
    return sample(iterable, len(iterable))


def read_table(filename: str, count: int = 1) -> str:
    """
    The functions either grabs a random line from a file if count is 1 or it grabs a sample of size
    count from the file instead. That second feature is only used for the quirks table in this file
    but it can be extended to any DND table you can imagine!
    """
    with open(f"tables/{filename}.txt", "r", encoding="UTF-8") as tmpfile:
        lines = [line.strip() for line in tmpfile.readlines()]

    if count == 1:
        return choice(lines)

    return " ".join(sample(lines, count))


def dice(size: int = 20) -> int:
    """
    This can be any dice in the game, and can easily be used for hp or attack rolls.
    x defaults to 20 for ease of use but I recommend using real dice for role-play and digital
    dice for mass generation.
    """
    if size < 2:
        print(f"The smallest dice you can roll is two sided but you tried {size}.")
        return 0
    return choice(range(1, size + 1))


def modify(stat: int) -> int:
    """
    This takes any stat value and returns it's modifier. You may also do this in your
    head but Python needs the formula.
    """
    return (stat - 10) // 2


def base_stats() -> dict:
    """
    You can modify the base stats for your whole project here. I wanted something like
    a class for this but I don't need dot access and so I realized a function that prefills
    a struct is all you need.
    """

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
    return stats


def apply_stats_bonuses(stats: dict, attributes: dict) -> dict:
    """
    Applies the entries in an attributes dict to the stats dict.

    This is only used for classes and races for now, but it can be extended to include
    new systems later and that's why I made it modular.
    """
    for pair in attributes:
        key, val = pair[0], pair[1]
        stats[key] += val
    return stats


def apply_stat_pool(stats: dict, npc: NPC) -> dict:
    """
    The calculates a pool of stats which starts at 22 (subtracting five for the class_bonuses).
    NPCs get an extra stat point per level beyond level 1 to boost their stats a bit. This can
    be modified per use case.

    After the stat pool is calculated this function cycles between the six dnd stats and adds
    one point each until the pool is empty. I also shuffle the dnd stat pool for each new character
    so that atk isn't the default highest stat for everyone!
    """

    pool: int = 22 + ((npc.level - 1) * 1)
    for stat in cycle(shuffled(["str", "int", "dex", "wis", "con", "cha"])):
        if pool < 1:
            break

        # You could put a stat ceiling here but I removed mine for simplicity.
        stats[stat] += 1
        pool -= 1
    return stats


def calc_hp(level: int, con: int, hit: int) -> int:
    """
    This is the standard DND HP formula per level. This can be used
    to calculate fully legal player character HP stats.

    All you need is the characters level, constitution and hit dice.
    """
    mod: int = modify(con)
    hp: int = mod + hit
    if level == 1:
        return hp

    for _ in range(level - 1):
        hp += mod + dice(hit)
    return hp


def generate_stats(npc: NPC) -> dict:
    """
    I don't really know where to put the two bonuses dicts they feel weirdly isolated as globals
    and I don't want to read them from a file because that makes distribution harder.

    So these function contains two bonuses dictionaries and it generates a fresh base_stat
    and then applies an NPCs bonuses and stat pool to calculate every stat they need to have.

    You have to track race/class abilities yourself. Things like dark-vision are not
    documented here but the books should have that info.

    The word "hit" refers to the hit dice for a given NPC throughout this function.
    """

    # These are base stat values given for each race.
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

    # This dict helps put a few stat points into an NPC's class
    # It also tracks the class based hit dice.
    class_bonuses: dict = {
        "Barbarian": [("con", 3), ("str", 2), ("hit", 12)],
        "Bard": [("cha", 3), ("int", 2), ("hit", 8)],
        "Cleric": [("wis", 3), ("cha", 2), ("hit", 8)],
        "Druid": [("wis", 3), ("dex", 2), ("hit", 8)],
        "Fighter": [("str", 3), ("con", 2), ("hit", 10)],
        "Monk": [("dex", 3), ("wis", 2), ("hit", 8)],
        "Paladin": [("cha", 3), ("str", 2), ("hit", 10)],
        "Ranger": [("str", 3), ("dex", 2), ("hit", 10)],
        "Rogue": [("dex", 3), ("cha", 2), ("hit", 8)],
        "Sorcerer": [("con", 3), ("int", 2), ("hit", 6)],
        "Warlock": [("int", 3), ("con", 2), ("hit", 8)],
        "Wizard": [("int", 3), ("wis", 2), ("hit", 6)],
    }

    # Start with a blank stat object!
    stats: dict = base_stats()
    stats = apply_stats_bonuses(stats, race_bonuses[npc.race])
    stats = apply_stats_bonuses(stats, class_bonuses[npc.job])
    stats = apply_stat_pool(stats, npc)

    # This is fully DND legal HP.
    stats["hp"] += calc_hp(npc.level, stats["con"], stats["hit"])

    # The base dc gets +1 every four levels.
    stats["dc"] += modify(stats["dex"]) + (npc.level // 4)

    return stats


if __name__ == "__main__":
    # No need for argv if this is being used as a module!
    from sys import argv

    # This cleverly handles the IndexError and the ValueError with the same default value.
    try:
        npc_level = int(argv[1])
    except:
        npc_level = 1

    print(NPC(level=npc_level))
