from itertools import combinations, product
from cg.game import Game


def load_games(path):
    """Load a list of games from a file.
    Each row in the file should represent one combinatorial game.
    The game should be in combinatorial game notation (CGN).

    Parameters
    ----------
    path : str
        Path to the file with games.

    Returns
    -------
    games : list
        The list of games in CGN as str.
    """
    with open(path) as f:
        return [line.strip() for line in f]


def incomparable_pairs(games):
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


def incomparable_subsets(incomp_pairs):
    """Generate all subsets without dominated options.

    Parameters
    ----------
    incomp_pairs : dict
        Dictionary of sets of str of games.
        Each dictionary item is a set of games that are incomparable
        with the game that is the corresponding key.

    Yields
    ------
    subset : set
        Subset of games without dominated options and at least one option.
    """
    empty_set = frozenset()
    found_subsets = {empty_set}
    for g in incomp_pairs:
        for sub in found_subsets.copy():
            # Check whether G is incomparable with all elements in the subset
            if sub <= incomp_pairs[g]:
                # All elements in sub are incomparable to G
                sub_with_g = frozenset(list(sub) + [g])
                found_subsets.add(sub_with_g)
                yield sub_with_g


# The following function was executed in C++ for speed
def subsets_to_games(subsets):
    """Create all games from subsets. The games are not in canonical form.
    Each L, R pair of possible subset pairs generates a game {L|R}.
    Both L and R are nonempty, except for the first game.
    For completeness, the first game yielded is {|} = 0

    Parameters
    ----------
    subsets : iterable
        The subsets to generate the games from. The games in the iterable
        are all in combinatorial game notation.

    Yields
    ------
    g : str
        A game in combinatorial game notation.

    Warnings
    --------
    The generated games are not in canonical form; duplicates are likely to occur.
    """
    yield "0"
    for left, right in product(subsets, repeat=2):
        g = "{" + ",".join(left) + "|" + ",".join(right) + "}"
        yield g


def to_canonical(games):
    """Convert games to their canoncial forms.

    Parameters
    ----------
    games : iterable
        The games to convert, each in combinatorial game notation.

    Yields
    ------
    canonical : str
        A game in canonical form.

    Notes
    -----
    The order of the converted games is preserverd.
    """
    for g in games:
        yield str(Game(g).canonical_form())


def filter_unique(games):
    """Keep only the unique games.

    Parameters
    ----------
    games : iterable
        The canonical forms to filter in combinatorial game notation.

    Yields
    ------
    unique_game : str
        A unique canonical form in CGN.

    Warnings
    --------
    It is assumed that the games' options are sorted lexicographically.
    """
    uniques = set()
    for g in games:
        # Add to set if not already in there
        if g not in uniques:
            uniques.add(g)
            yield g


if __name__ == "__main__":
    # Load games from file
    games_in_g0x = load_games("groups_research/results/g02.txt")

    # For each game, compute the games it is incomparable to
    inc_pairs = incomparable_pairs(games_in_g0x)

    # Generate all subsets with only incomparable options
    inc_subsets = incomparable_subsets(inc_pairs)

    # Write to file
    with open("groups_research/results/inc_subsets_from_g02.txt", "w") as f:
        for i, sub in enumerate(inc_subsets):
            f.write(";".join(sub) + "\n")

    # Generate all games using these sets
    # Note, this was actually done using a C++ program
    # all_games = subsets_to_games(inc_subsets)
