import multiprocessing as mp
from datetime import datetime
from tqdm import tqdm
from cg.game import Game

GROUP = 4
INPUT_FILE = f"groups_research/results/all_possible_g0{GROUP:d}.txt"
OUTPUT_FILE = f"groups_research/results/all_canonicals_g0{GROUP:d}.txt"
NUM_CORES = 24


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
        return [line.strip() for line in tqdm(f, unit="games")]


def to_canonical_cgn(game):
    """Convert a game to its canoncial form in CGN.

    Parameters
    ----------
    game : str
        The game to convert in combinatorial game notation.
    """
    canonical = str(Game(game).canonical_form())
    return f"{datetime.now():%Y-%m-%d %H:%M:%S};{mp.current_process().name};{game};{canonical}\n"


def reduce_game_list(games):
    """Reduce an iterator of games to their canonical forms.
    The games are reduces in parallel using multiprocessing.

    Parameters
    ----------
    games : iterator
        The games that are to be reduced.

    Warnings
    --------
    The order of games of the input iterator is NOT preserved.
    """
    TOTAL_GAMES = len(games)
    pool = mp.Pool(NUM_CORES)
    pool_returns = pool.imap_unordered(to_canonical_cgn, games, chunksize=1024)
    return list(tqdm(pool_returns, total=TOTAL_GAMES, unit="games"))


if __name__ == "__main__":
    # Load games from file
    print(f"{datetime.now():%Y-%m-%d %H:%M:%S}: Loading input file '{INPUT_FILE}'.")
    all_games = load_games(INPUT_FILE)
    print(f"{datetime.now():%Y-%m-%d %H:%M:%S}: Finished loading input file, loaded {len(all_games):d} games.")

    # Convert all of these to canonical forms
    print(f"{datetime.now():%Y-%m-%d %H:%M:%S}: Converting games to non-unique canonical games.")
    canonicals = reduce_game_list(all_games)
    print(f"{datetime.now():%Y-%m-%d %H:%M:%S}: Finished computing games and their non-unique canonical forms.")

    # Write them to file
    print(f"{datetime.now():%Y-%m-%d %H:%M:%S}: Writing results to output file '{OUTPUT_FILE}'.")
    with open(OUTPUT_FILE, "w", newline="\n") as f:
        f.write("idx,timestamp;proc_id;game;canonical\n")
        for line in tqdm(canonicals, unit="games"):
            f.write(line)
    print(f"{datetime.now():%Y-%m-%d %H:%M:%S}: Finished writing results to output file.")
