from datetime import datetime
from itertools import combinations, product
import multiprocessing as mp

from cg.game import Game

NUM_CORES = 3


def read_games_file(path: str) -> list:
    """Read games from a file.
    Each row in the file should represent one combinatorial game.
    The game should be in combinatorial game notation (CGN).

    Parameters
    ----------
    path : str
        Path of the file containing the CGN games.

    Returns
    -------
    games_list : list of str
        List of games, each game is represented by its CGN.
    """
    with open(path) as f:
        return [line.strip() for line in f]


def get_incomparable_pairs(games: list) -> dict:
    """Compute incomparable pairs in a list of games.

    Parameters
    ----------
    games : list
        List of games. Each game is represented as str in CGN.

    Returns
    -------
    incomparable_pairs : dict
        Dictionary of sets of str of games.
        Each dictionary item is a set of games that are incomparable
        with the game that is the corresponding key.
    """
    incomparable_pairs = dict()
    # Create keys with empty sets
    for g in games:
        incomparable_pairs[g] = set()

    # Check combinations
    for g, h in combinations(games, r=2):
        if Game(g).incomparable(Game(h)):
            incomparable_pairs[g].add(h)
            incomparable_pairs[h].add(g)

    # Return the dictionary
    return incomparable_pairs


def add_with_allowed_games(current: list, allowed: set, incomp_pairs: dict, results: list):
    if not allowed:
        yield current.copy()

    # Do and do not add each incomparable game
    while allowed:
        # Get the next incomparable game
        g = allowed.pop()

        # Add to current list and check
        current.append(g)
        new_allowed = allowed & incomp_pairs[g]
        yield from add_with_allowed_games(current, new_allowed, incomp_pairs, results)
        current.remove(g)

        # Check without G in set
        yield from add_with_allowed_games(current, allowed, incomp_pairs, results)


def generate_incomparable_subsets(games: list, incomp_pairs: dict):
    results = []
    games_so_far = set()
    for g in games:
        games_so_far.add(g)
        # Only add games to this list that have not yet been checked
        allowed_to_add = incomp_pairs[g] - games_so_far
        # Start generating subsets, starting with the current game G
        yield from add_with_allowed_games([g], allowed_to_add, incomp_pairs, results)


def generate_games_from_subsets(subsets: list):
    yield "0"
    for left, right in product(subsets, repeat=2):
        g = Game()
        # Add all options from the sets to the game
        if left:
            g.left_options.extend(Game(opt) for opt in left)
        if right:
            g.right_options.extend(Game(opt) for opt in right)

        # Yield the canonical form as str
        yield str(g.canonical_form())


def filter_canonicals(canonicals):
    """Keep only the unique canonical forms.
    """
    uniques = set()
    for g in canonicals:
        # Add to set if not already in there
        if g not in uniques:
            uniques.add(g)
            ts = datetime.now().strftime(r"%Y-%m-%d %H:%M:%S")
            print(f"{ts}: Unique canonical form {len(uniques):d}:", g)

    # Return the unique (sorted) canonical forms
    ts = datetime.now().strftime(r"%Y-%m-%d %H:%M:%S")
    print(f"{ts}: Unique canonical forms: {len(uniques):d}")
    return uniques


def canonical_from_pair(pair: tuple):
    # Split pair in left and right options
    left, right = pair
    g = Game()
    # Add all options from the sets to the game
    if left:
        g.left_options.extend(Game(opt) for opt in left)
    if right:
        g.right_options.extend(Game(opt) for opt in right)

    # Return the canonical form as str
    return str(g.canonical_form())


def parallel_generate_games(subset_generator):
    # First, yield the zero game
    yield "0"

    pair_generator = product(subset_generator, repeat=2)
    print(f"Generating games using {NUM_CORES:d} cores.")
    pool = mp.Pool(NUM_CORES)
    canonicals_iterator = pool.imap(canonical_from_pair, pair_generator, chunksize=64)

    # Count and yield the generated games
    count_games = 0
    for canon in canonicals_iterator:
        count_games += 1
        yield canon

    ts = datetime.now().strftime(r"%Y-%m-%d %H:%M:%S")
    print(f"{ts}: Non-unique canoncial games: {count_games:d}.")


if __name__ == "__main__":
    games_in_g0x = read_games_file("groups_research/results/g02.txt")
    inc_pairs = get_incomparable_pairs(games_in_g0x)
    incomparable_subset_gen = generate_incomparable_subsets(games_in_g0x, inc_pairs)
    canonicals_gen = parallel_generate_games(incomparable_subset_gen)
    filter_canonicals(canonicals_gen)
