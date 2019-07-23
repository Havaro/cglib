from itertools import combinations, permutations, product
from multiprocessing import Pool, Manager

from cg.game import Game

NUM_PROC = 3


def checkSubset(subset_di):
    subset, di = subset_di
    for option_pair in permutations(subset, 2):
        # Check whether this pair was seen before
        outcome = di.get(option_pair)

        if outcome is None:
            # These games were not compared before
            outcome = Game(option_pair[0]).geq(Game(option_pair[1]))
            # Add to dict
            di[option_pair] = outcome

        if outcome:
            # option_pair[0] >= option_pair[1], subset contains dominated options
            return None

    # No dominated options, return this set
    return subset


def filterDominatedSubsets(subsetgenerator):
    # Create multiprocessing pool to check for nondominated subsets
    print("Filtering dominated using a pool with {:d} processes.".format(NUM_PROC))
    nondominated = []
    pool = Pool(NUM_PROC)

    # Multiprocess the subsets and append them if they do not have dominated options
    # i.e. the result is not None
    for sub in pool.imap_unordered(checkSubset, ((s, str_geq_pairs) for s in subsetgenerator), chunksize=32):
        if sub is not None:
            nondominated.append(sub)
            print("Found nondominated set {:d}:".format(len(nondominated)), *sub)

    # Return nondominated subsets
    return nondominated


def getAllSubsets(canonicals: list):
    for gen in (combinations(canonicals, curl) for curl in range(1, len(canonicals) + 1)):
        for comb in gen:
            yield comb


def computeCombinations(sets):
    yield "0"
    # Create the cartesian product to create all combinations
    # of Left and Right option sets.
    for leftSet, rightSet in product(sets, repeat=2):
        g = Game()
        # Add all options from the sets to the game
        if leftSet:
            g.leftOptions.extend(Game(opt) for opt in leftSet)
        if rightSet:
            g.rightOptions.extend(Game(opt) for opt in rightSet)

        # Yield the canonical form
        yield str(g.canonicalForm())


def filter_unique_canonicals(str_canons):
    str_uniques = []
    for g in str_canons:
        already = False
        for h in str_uniques:
            # Check whether G >= H was checked before
            ggeqh = str_geq_pairs.get((g, h))
            if ggeqh is None:
                # It was not
                ggeqh = Game(g).geq(Game(h))
                str_geq_pairs[(g, h)] = ggeqh

            # If G >= H, it might be that G == H
            if ggeqh:
                # Check whether H >= G was checked before
                hgeqg = str_geq_pairs.get((h, g))
                if hgeqg is None:
                    # It was not
                    hgeqg = Game(h).geq(Game(g))
                    str_geq_pairs[(h, g)] = hgeqg

                # Check whether G == H
                if hgeqg:
                    # Already in list, skip
                    already = True
                    break

        # Was G not already in the list?
        if not already:
            str_uniques.append(g)
            print("Canonical form {:d}:".format(len(str_uniques)), g)

    # Return the set of unique canonical forms
    return str_uniques


def G0(depth: int = 1):
    subsets = ["0"]
    for i in range(depth):
        print("Depth is now {:d}.".format(i + 1))

        # Find all subsets
        print("Creating the subset generator.")
        subsets = getAllSubsets(subsets)
        # print('There are {:d} subsets:'.format(len(subsets)), *subsets)

        # Remove sets with dominated options
        print("Filtering the non-dominated subsets.")
        nondomsets = filterDominatedSubsets(subsets)
        print("There are {:d} subsets without any dominated options.".format(len(nondomsets)))

        # Compute the number of games with Left and Right a subset
        print("The number of possible games is {size:d}^2+1={tot:d}.".format(size=len(nondomsets), tot=len(nondomsets) ** 2 + 1))

        # Find all of their canonical forms
        print("Creating the canonical form generator.")
        canons = computeCombinations(nondomsets)

        # Print the canonical forms and add them to a list for the next iteration
        print("Filtering unique canonical forms.")
        subsets = filter_unique_canonicals(canons)
        # print('There are {:d} unique canonical forms:'.format(len(canons)), *canons)


if __name__ == "__main__":
    m = Manager()
    str_geq_pairs = m.dict()

    G0(3)
