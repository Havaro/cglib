from multiprocessing import Pool, Queue, Process, current_process
from tqdm import tqdm
from datetime import datetime
from itertools import combinations, product
from cg.game import Game

GROUP = 4
INPUT_FILE = f"groups_research/results/g0{GROUP-1:d}.txt"
OUTPUT_FILE = f"groups_research/results/all_canonicals_g0{GROUP:d}.txt"
NUM_PROC = 256


def read_file(path):
    """Load a list of items from a file.
    Each row in the file should represent one item.

    Parameters
    ----------
    path : str
        Path to the file.

    Returns
    -------
    items : list
        The list of items in the file as :py:class:`str`.
    """
    print(f"{datetime.now():%Y-%m-%d %H:%M:%S}: Reading file '{path}'.")
    with open(path, "r") as f:
        return [line.strip() for line in tqdm(f, unit="lines")]


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
    print(f"{datetime.now():%Y-%m-%d %H:%M:%S}: Checking for incomparable pairs.")
    incomparable_pairs = dict()
    # Create keys with empty sets
    for g in games:
        incomparable_pairs[g] = set()

    # Check combinations
    num_inc = 0
    num_comb = int(len(games) * (len(games) - 1) / 2)
    for g, h in tqdm(combinations(games, r=2), total=num_comb, unit="pairs"):
        if Game(g).incomparable(Game(h)):
            incomparable_pairs[g].add(h)
            incomparable_pairs[h].add(g)
            num_inc += 1

    print(f"{datetime.now():%Y-%m-%d %H:%M:%S}: {num_inc:d} incomparable pairs found.")
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
    print(f"{datetime.now():%Y-%m-%d %H:%M:%S}: Generating incomparable subsets.")
    empty_set = frozenset()
    found_subsets = {empty_set}
    for g in tqdm(incomp_pairs, unit="incomp_pairs"):
        for sub in tqdm(found_subsets.copy(), unit="subsets"):
            # Check whether G is incomparable with all elements in the subset
            if sub <= incomp_pairs[g]:
                # All elements in sub are incomparable to G
                sub_with_g = frozenset(list(sub) + [g])
                found_subsets.add(sub_with_g)
                yield sub_with_g


def canonical_from_pair(pair):
    """Convert a game to its canoncial form in CGN.

    Parameters
    ----------
    pair : tuple
        The left and right options.

    Returns
    ------
    info : str
        Information about the generated game and its canonical form.
    """
    g = Game()
    g.left_options = [Game(opt) for opt in pair[0]]
    g.right_options = [Game(opt) for opt in pair[1]]
    canonical = g.canonical_form()
    return f"{datetime.now():%Y-%m-%d %H:%M:%S};{current_process().name};{str(g)};{str(canonical)}\n"


def writer(q_in, data_it, data_len):
    for d in tqdm(data_it, total=data_len, unit="pairs"):
        # for d in data_it:
        q_in.put(d)
    for i in range(NUM_PROC):
        q_in.put(None)
    print(f"{datetime.now():%Y-%m-%d %H:%M:%S}: Finished generating pairs for input queue.")


def worker(q_in, q_out):
    while True:
        pair = q_in.get(True)
        if pair:
            # Process pair
            q_out.put(canonical_from_pair(pair))
        else:
            # No jobs left, put sentinel value
            q_out.put(None)
            break


def canonicals_from_subsets(subsets):
    """Create games from all possible combinations of subsets from an iterator.
    The games are reduced to canonical form in parallel using multiprocessing.

    Parameters
    ----------
    subsets : iterator
        The subsets that are to be combined.

    Returns
    -------
    canonicals : iterator
        Generator of the information strings about the computed canonical froms.

    Warnings
    --------
    * The order of games of the input iterator is NOT preserved.
    * It is likely that many duplicate games are created.
    """
    print(f"{datetime.now():%Y-%m-%d %H:%M:%S}: Generating games from subsets to non-unique canonical games.")
    pair_generator = product(subsets, repeat=2)

    # Create queues
    q_in = Queue()
    q_out = Queue()

    # Start processes
    pool = Pool(NUM_PROC, worker, (q_in, q_out))

    # Fill queue
    print(f"{datetime.now():%Y-%m-%d %H:%M:%S}: Generating all pairs for input queue.")
    proc_w = Process(target=writer, args=(q_in, pair_generator, len(subsets)**2))
    proc_w.start()

    # Return values from output queue
    print(f"{datetime.now():%Y-%m-%d %H:%M:%S}: Waiting for results to finish.")
    num_finished = 0
    with tqdm(total=len(subsets)**2, unit="canonics", position=1) as pbar:
        while num_finished < NUM_PROC:
            res = q_out.get()
            if res:
                pbar.update(1)
                yield res
            else:
                num_finished += 1

    # Wait for jobs to finish
    proc_w.join()
    pool.close()
    pool.join()


def write_iterator(path, lines, num_lines=None):
    """Write lines to a file.

    Parameters
    ----------
    path : str
        The file to write the lines to.

    lines : iterator
        The lines to write to the file.

    num_lines : int, optional
        The number of lines to write. Used to indicate an ETA.
        When :py:data:`None`, no ETA of writing is given.

    Warnings
    --------
    The file specified by `path` will be overwritten if already exists.
    """
    print(f"{datetime.now():%Y-%m-%d %H:%M:%S}: Writing results to output file '{path}'.")
    f = open(path, "w", newline="\n")
    f.write("idx;timestamp;proc_id;game;canonical\n")
    for i, res in enumerate(tqdm(lines, total=num_lines, unit="lines", position=2), start=1):
        f.write(f"{i:d};{res}")
    f.close()


if __name__ == "__main__":
    # Load games from previous group
    games_in_g0x = read_file(INPUT_FILE)

    # Compute all incomparable pairs
    inc_pairs = incomparable_pairs(games_in_g0x)

    # Generate all subsets with only incomparable options
    inc_subsets = list(incomparable_subsets(inc_pairs))

    # Generate all games from these subsets
    canonical_gen = canonicals_from_subsets(inc_subsets)

    # Empty iterator to file
    write_iterator(OUTPUT_FILE, canonical_gen, len(inc_subsets)**2)

    # End of program
    print(f"{datetime.now():%Y-%m-%d %H:%M:%S}: Finished writing results to output file.")
