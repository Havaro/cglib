from datetime import datetime


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
    print("timestamp;number;unique")
    uniques = set()
    for g in games:
        # Add to set if not already in there
        if g not in uniques:
            uniques.add(g)
            print(f"{datetime.now():%Y-%m-%d %H:%M:%S};{len(uniques):d};{g}")
            yield g


if __name__ == "__main__":
    # Load games from file
    print(f"{datetime.now():%Y-%m-%d %H:%M:%S}: Loading g0x file.")
    all_canons = load_games("groups_research/results/all_canonicals_g04.txt")
    print(f"{datetime.now():%Y-%m-%d %H:%M:%S}: Finished loading g0x file, loaded {len(all_canons):d} canonicals.")

    # Filter unique (in this case canonical) forms and count
    print(f"{datetime.now():%Y-%m-%d %H:%M:%S}: Filtering unique canonical forms.")
    uniques = list(filter_unique(all_canons))
    print(f"{datetime.now():%Y-%m-%d %H:%M:%S}: Finished filtering to {len(uniques):d} unique canonical forms.")
