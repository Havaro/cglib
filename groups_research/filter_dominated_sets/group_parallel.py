from itertools import combinations, permutations, product
from multiprocessing import Pool

from cg.game import Game

NUM_PROC = 64


def check_subset(subset):
    for option_pair in permutations(subset, 2):
        if option_pair[0].geq(option_pair[1]):
            return None
    return subset


def filterDominatedSubsetsPar(subsetgenerator):
    # Create multiprocessing pool to check for nondominated subsets
    print("Filtering dominated using a pool with {:d} processes.".format(NUM_PROC))
    nondominated = []
    pool = Pool(NUM_PROC)

    # Multiprocess the subsets and append them if they do not have dominated options
    # i.e. the result is not None
    for sub in pool.imap_unordered(check_subset, subsetgenerator, chunksize=32):
        if sub is not None:
            nondominated.append(sub)
            print("Found nondominated set {:d}:".format(len(nondominated)), *sub)

    # Return nondominated subsets
    return nondominated


def filterDominatedSubsetsSeq(subsetgenerator):
    print("Filtering dominated sequentially.")
    checks = [check_subset(sub) for sub in subsetgenerator]
    return [c for c in checks if c]


def getAllSubsets(canonicals: list):
    for gen in (combinations(canonicals, curl) for curl in range(1, len(canonicals) + 1)):
        for comb in gen:
            yield comb


def compute_combinations(sets):
    yield Game("0")
    # Create the cartesian product to create all combinations
    # of Left and Right option sets.
    for left_set, right_set in product(sets, repeat=2):
        g = Game()
        # Add all options from the sets to the game
        if left_set:
            g.left_options.extend(left_set)
        if right_set:
            g.right_options.extend(right_set)

        # Yield the canonical form
        yield g.canonical_form()


def G0(depth: int = 1):
    subsets = [Game("0")]
    for i in range(depth):
        print("Depth is now {:d}.".format(i + 1))

        # Find all subsets
        print("Creating the subset generator.")
        subsets = getAllSubsets(subsets)
        # print('There are {:d} subsets:'.format(len(subsets)), *subsets)

        # Remove sets with dominated options
        print("Filtering the non-dominated subsets.")
        nondomsets = filterDominatedSubsetsPar(subsets)
        print("There are {:d} subsets without any dominated options.".format(len(nondomsets)))

        # Compute the number of games with Left and Right a subset
        print("The number of possible games is {size:d}^2+1={tot:d}.".format(size=len(nondomsets), tot=len(nondomsets) ** 2 + 1))

        # Find all of their canonical forms
        print("Creating the canonical form generator.")
        canons = compute_combinations(nondomsets)

        # Print the canonical forms and add them to a list for the next iteration
        # TODO: Parallelize?
        print("Filtering unique canonical forms.")
        subsets = []
        for g in canons:
            if g not in subsets:
                # Only keep unique canonical forms
                subsets.append(g)
                print("Canonical form {:d}:".format(len(subsets)), g)
        # print('There are {:d} unique canonical forms:'.format(len(canons)), *canons)


if __name__ == "__main__":
    G0(4)
