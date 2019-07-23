import multiprocessing as mp
from cg.game import Game
from datetime import datetime
from tqdm import tqdm

GROUP = 3
INPUT_FILE = f"groups_research/results/g0{GROUP:d}.txt"
OUTPUT_FILE = f"groups_research/results/results_compute_center_g0{GROUP:d}.csv"
NUM_CORES = 24


def read_games(path):
    print("Reading games...")
    with open(path) as f:
        return [line.strip() for line in tqdm(f, unit="games")]


def structure_center_type(cgn):
    """Check whether a dicotic game is in the center.

    Parameters
    ----------
    cgn : str
        Dicotic game in combinatorial game notation.

    Returns
    -------
    center_type : {"not_center", "own_inverse", "inv_incomp"}
        The center type determines what kind of game in the center it is:
        * "not_center" : This game is not in the center
        * "own_inverse" : The game is equal to its own inverse and is therefore in the center.
        * "inv_incomp" : The game is incomparable with its own inverse and therefore in the center.
    """
    # Create the game and compute its inverse
    g = Game(cgn)
    h = g.inverse()
    # Check whether this game is it's own inverse
    if str(g) == str(h):
        return "own_inverse"
    # Check whether the game is incomparable with its inverse
    if g.incomparable(h):
        return "inv_incomp"
    # This game is not in the center
    return "not_center"


def worker(cgn):
    # Process this game
    ctype = str(structure_center_type(cgn))
    proc_name = mp.current_process().name
    return f"{datetime.now():%Y-%m-%d %H:%M:%S};{proc_name};{cgn};{ctype}\n"


def exec_parallel(games):
    # Start the multiprocessing
    pool = mp.Pool(NUM_CORES)
    it = pool.imap_unordered(worker, games)
    # Fetch the results
    print("Fetching results...")
    return list(tqdm(it, desc="Computing center", unit="games", total=len(games)))


def output_results(res_lines, outfile):
    print("Writing to output file...")
    with open(OUTPUT_FILE, "w") as f:
        f.write("timestamp;proc_name;game;center_type\n")
        for line in res_lines:
            f.write(line)


all_games = read_games(INPUT_FILE)
res_it = exec_parallel(all_games)
output_results(res_it, OUTPUT_FILE)
