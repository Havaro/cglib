import re


def expand_stars(cgn):
    """Expand stars to full combinatorial game notation.

    Parameters
    ----------
    cgn : str
        The CNG that may contain star games.

    Returns
    -------
    star_expanded : str
        The CGN string with expanded stars.
    """
    regex = re.compile(r"\*(\d*)")
    match = re.search(regex, cgn)
    while match:
        # A star has been found
        if match.group(1):
            # The star has a number after it
            star_num = int(match.group(1))
        else:
            # No number -> *1
            star_num = 1

        # Replace the star
        expanded_star = "0"
        for i in range(1, star_num):
            expanded_star += ",*" + str(i)
        replace_game = "{" + expanded_star + "|" + expanded_star + "}"
        cgn = cgn.replace(match.group(0), replace_game, 1)

        # Find the next match
        match = re.search(regex, cgn)

    # No stars are left, return the resulting cgn
    return cgn


def expand_integers(cgn):
    """Expand integers to full combinatorial game notation.

    Parameters
    ----------
    cgn : str
        The CGN that may contain integer games.

    Returns
    -------
    int_expanded : str
        The CGN string with expanded integers.
    """
    regex = re.compile(r"(-?\d+)")
    match = regex.search(cgn)
    while match:
        # A match has been found
        int_val = int(match.group(1))
        # Create the expanded form
        replaced_num = "{|}"
        if int_val >= 0:
            for _ in range(int_val):
                replaced_num = "{" + replaced_num + "|}"
        else:
            for _ in range(-int_val):
                replaced_num = "{|" + replaced_num + "}"
        # Replace the integer
        cgn = cgn[: match.start()] + replaced_num + cgn[match.end() :]
        # Find the next match
        match = regex.search(cgn)
    # No matches left, return cgn without integers
    return cgn


def expand_cgn(compressed_cgn):
    """Expand a compressed combinatorial game notation string.
    Replaces known games by their extended forms.
    After replacement, the CGN should only contain '{', ',', '|' and '}'.

    Parameters
    ----------
    compressed_cgn : str
        The combinatorial game notation string to expand.

    Returns
    -------
    expanded : str
        The CGN with all known games replaced.
    """
    expanded = compressed_cgn

    # Words to characters
    expanded = expanded.replace("up", "^")
    expanded = expanded.replace("down", "v")
    expanded = expanded.replace("star", "*")
    expanded = expanded.replace("zero", "0")

    expanded = expanded.replace("v*", "{0|0,*}")
    expanded = expanded.replace("^*", "{0,*|0}")

    expanded = expanded.replace("v", "{*|0}")
    expanded = expanded.replace("^", "{0|*}")

    # Replace *n's
    expanded = expand_stars(expanded)
    # Replace integer games
    expanded = expand_integers(expanded)

    # The resulting game should be valid expanded CGN
    if not is_valid_expanded_cgn(expanded):
        raise ValueError(f"Invalid cgn string. Parts are not expanded: '{expanded}'")
    return expanded


def compress_cgn(cgn):
    """Compress an extended combinatorial game notation string.
    Replaces some known games by their abbreviations.
    It is assumed that the options are sorted lexicographically .

    Parameters
    ----------
    cgn : str
        The CGN to compress. The options have to be sorted .

    Returns
    -------
    compressed : str
        The CGN in compressed form.
    """
    compressed = cgn

    # Games to characters
    compressed = compressed.replace("{|}", "0")

    compressed = compressed.replace("{0|0}", "*")
    compressed = compressed.replace("{*,0|*,0}", "*2")
    compressed = compressed.replace("{*,*2,0|*,*2,0}", "*3")

    compressed = compressed.replace("{0|*}", "^")
    compressed = compressed.replace("{*|0}", "v")

    compressed = compressed.replace("{*,0|0}", "^*")
    compressed = compressed.replace("{0|*,0}", "v*")

    compressed = compressed.replace("{0|}", "1")
    compressed = compressed.replace("{|0}", "-1")
    return compressed


def is_valid_expanded_cgn(expanded_cgn):
    """Checks whether a :py:class:`str` is in expanded combinatorial game notation.

    A valid expanded CGN contains only '{', ',', '|' and '}'.
    The number of '{' is equal to the number of '|' and '}'.

    Parameters
    ----------
    expanded_cgn : str
        The CGN string to check.

    Returns
    -------
    valid : bool
        :py:const:`True` when the CGN is valid, :py:const:`False` otherwise.
    """
    if not expanded_cgn:
        return False

    left = expanded_cgn.count("{")
    center = expanded_cgn.count("|")
    right = expanded_cgn.count("}")

    if left != center or right != center:
        return False

    for c in expanded_cgn:
        if c != "{" and c != "|" and c != "}" and c != ",":
            return False
    return True
