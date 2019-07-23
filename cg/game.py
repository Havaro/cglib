import cg.game_notations as gn


class Game:
    def __init__(self, cgn=""):
        self.left_options = []
        self.right_options = []

        # Speed up if 0-game
        if cgn and cgn != "0" and cgn != "zero":
            self.set_cgn(cgn)

    def __str__(self):
        return self.get_cgn()

    def __repr__(self):
        return str(self)

    def clear(self):
        self.left_options.clear()
        self.right_options.clear()

    # Clone a game by duplicating the game tree recursively
    # Replaces/implements deepcopy functionality
    def clone(self):
        c = Game()
        c.left_options = [option.clone() for option in self.left_options]
        c.right_options = [option.clone() for option in self.right_options]
        return c

    def _set_node_cgn(self, expanded_cgn, index):
        """Create a Game from expanded cgn.

        Assumes the `expanded_cgn` is in expanded combinatorial game notation.
        Only characters '{', ',', '|' and '}' are valid.

        Parameters
        ----------
        expanded_cgn : str
            The game in CGN that this node is part of.

        index : int
            The index in expanded_cgn that this node represents.
        """
        letter = expanded_cgn[index]
        currently_left = True
        while letter != "}":
            if letter == "{":
                opt = Game()
                index += 1
                index = opt._set_node_cgn(expanded_cgn, index=index)
                if currently_left:
                    self.left_options.append(opt)
                else:
                    self.right_options.append(opt)
            elif letter == "|":
                currently_left = False

            # In the other cases (',' or '}'), do nothing
            # Go to the next letter
            index += 1
            letter = expanded_cgn[index]
        return index

    def set_cgn(self, cgn):
        self.clear()
        expanded = gn.expand_cgn(cgn)
        self._set_node_cgn(expanded, 1)
        return self

    def get_cgn(self):
        return self._get_node_cgn()

    def _get_node_cgn(self):
        # Get and sort all left options
        left_list = sorted([opt._get_node_cgn() for opt in self.left_options])
        # Get and sort all right options
        right_list = sorted([opt._get_node_cgn() for opt in self.right_options])
        # Compress and return
        return gn.compress_cgn("{" + ",".join(left_list) + "|" + ",".join(right_list) + "}")

    def get_cgn_dot(self):
        return "digraph Game {\n" + self._get_node_cgn_dot("", 0)[0] + "}"

    def _get_node_cgn_dot(self, dot, index):
        me = index
        dot += f'\t{me:d}[label="{self}"];\n'
        for lo in self.left_options:
            dot, new_index = lo._get_node_cgn_dot(dot, index + 1)
            dot += f'\t{me:d} -> {index+1:d}[label="L"];\n'
            index = new_index
        for ro in self.right_options:
            dot, new_index = ro._get_node_cgn_dot(dot, index + 1)
            dot += f'\t{me:d} -> {index+1:d}[label="R"];\n'
            index = new_index
        return dot, index

    # Greater than or equal to zero (right starts -> loses)
    # None of Right's options can be leq_zero
    def geq_zero(self):
        for option in self.right_options:
            if option.leq_zero():
                return False
        return True

    # Less than or equal to zero (left starts -> loses)
    # None of Left's options can be geq_zero
    def leq_zero(self):
        for option in self.left_options:
            if option.geq_zero():
                return False
        return True

    # Greater than or incomparable to zero (left starts -> wins)
    # There must be a Left option geq_zero
    def gin_zero(self):
        for option in self.left_options:
            if option.geq_zero():
                return True
        return False

    # Less than or incomparable to zero (right starts -> wins)
    # There must be a Right option leq_zero
    def lin_zero(self):
        for option in self.right_options:
            if option.leq_zero():
                return True
        return False

    # Greater than zero (Left player win)
    def gtr_zero(self):
        return self.geq_zero() and self.gin_zero()

    # Less than zero (Right player win)
    def lss_zero(self):
        return self.leq_zero() and self.lin_zero()

    # Equal to zero (second player win)
    def equal_zero(self):
        return self.geq_zero() and self.leq_zero()

    # Incomparable to zero (first player win)
    def incomparable_zero(self):
        return self.gin_zero() and self.lin_zero()

    # Inverse: Swap Left and Right options recursively
    # Deepcopy is required, since the inverse is applied top-down
    def inverse(self):
        inv = self.clone()
        # Swap Left and Right options
        inv.left_options, inv.right_options = inv.right_options, inv.left_options
        # Invert all options
        inv.left_options = [lo.inverse() for lo in inv.left_options]
        inv.right_options = [ro.inverse() for ro in inv.right_options]
        return inv

    # Add: Add two games together
    # No deepcopy is required, since the new game is
    # constructed from new zero games recursively
    def add(self, other):
        s = Game()
        left_self = [slo.add(other) for slo in self.left_options]
        left_other = [self.add(olo) for olo in other.left_options]
        s.left_options = left_self + left_other
        right_self = [sro.add(other) for sro in self.right_options]
        right_other = [self.add(oro) for oro in other.right_options]
        s.right_options = right_self + right_other
        return s

    def subtract(self, other):
        return self.add(other.inverse())

    # Overloads
    def __eq__(self, other):
        return self.equal(other)

    def __add__(self, other):
        return self.add(other)

    def __sub__(self, other):
        return self.subtract(other)

    def __neg__(self):
        return self.inverse()

    # Check whether G>=H, True when G-H>=0
    def geq(self, other):
        return (self - other).geq_zero()

    # Check whether G<=H, True when G-H<=0
    def leq(self, other):
        return (self - other).leq_zero()

    # Check whether G>~H, True when G-H>~0
    def gin(self, other):
        return (self - other).gin_zero()

    # Check whether G<~H, True when G-H<~0
    def lin(self, other):
        return (self - other).lin_zero()

    # Check whether G>H, True when G-H>0
    def gtr(self, other):
        return (self - other).gtr_zero()

    # Check whether G<H, True when G-H<0
    def lss(self, other):
        return (self - other).lss_zero()

    # Check whether G=H, True when G-H=0
    def equal(self, other):
        return (self - other).equal_zero()

    # Check whether G~H, True when G-H~0
    def incomparable(self, other):
        return (self - other).incomparable_zero()

    def outcome_class(self):
        """Get the outcome class of the game.

        Returns
        -------
        outcome_class : str
            The letter defining the outcome class of the game G:
            * "N" when G is a win for the first player.
            * "P" when G is a win for the second player.
            * "L" when G is a win for Left
            * "R" when G is a win for Right
        """
        if self.geq_zero():
            # >= 0 -> P or L
            if self.leq_zero():
                # >= 0 and <= 0 -> P
                return "P"
            else:
                # >= 0 and >~ 0 -> L
                return "L"
        else:
            # <~ 0 -> R or N
            if self.leq_zero():
                # <~ 0 and <= 0 -> R
                return "R"
            else:
                # <~ 0 and >~ 0 -> N
                return "N"

    def companion(self):
        """Compute the companion of the game.

        The companion of a game is defined as follows:
            * * if G is a win for the second player
            * {0, companion(G^L)|companion(G^R)} if G is a win for Left
            * {companion(G^L)|0, companion(G^R)} if G is a win for Right
            * {companion(G^L)|companion(G^R)}
        Where G^L and G^R range over the options for Left and Right respectively.

        Returns
        -------
        comp : Game
            The companion of the game.
        """
        outcome = self.outcome_class()
        if outcome == "P":
            # The companion of a game G=0 is simply *
            return Game("*")

        # Create a new companion with all options as companion
        comp = Game()
        # Add all option's companions
        comp.left_options += [gl.companion() for gl in self.left_options]
        comp.right_options += [gr.companion() for gr in self.right_options]

        # Add 0 options based on outcome class
        if outcome == "L":
            # G is a win for Left
            comp.left_options.append(Game())
        elif outcome == "R":
            # G is a win for Right
            comp.right_options.append(Game())

        # Return the resulting companion
        return comp

    # Remove dominated options
    def remove_dominated(self, return_change=False):
        nodom = Game()
        change = False
        # Check Left options
        for lc1, lo1 in enumerate(self.left_options):
            for lo2 in self.left_options[lc1 + 1 :] + nodom.left_options:
                if lo2.geq(lo1):
                    # lo1 is dominated by lo2
                    change = True
                    break
            else:
                # lo1 was not dominated
                nodom.left_options.append(lo1.clone())

        # Check Right options
        for rc1, ro1 in enumerate(self.right_options):
            for ro2 in self.right_options[rc1 + 1 :] + nodom.right_options:
                if ro2.leq(ro1):
                    # ro1 is dominated by ro2
                    change = True
                    break
            else:
                # ro1 was not dominated
                nodom.right_options.append(ro1.clone())

        # Return the game without dominated options
        if return_change:
            return nodom, change
        return nodom

    # Replace reversible options
    def replace_reversible(self, return_change=False):
        reprev = Game()
        change = False
        # Check Left options
        for lo in self.left_options:
            # Loop all Right options of this Left option
            rev = False
            for lro in lo.right_options:
                # Check whether LR <= G
                if lro.leq(self):
                    # L is reversible through LR, replace with LR's Left options
                    change = rev = True
                    reprev.left_options.extend([lrl.clone() for lrl in lro.left_options])
            if not rev:
                # Left option was not reversible, leave it intact
                reprev.left_options.append(lo.clone())

        # Check Right options
        for ro in self.right_options:
            # Loop all Left options of this Right option
            rev = False
            for rlo in ro.left_options:
                # Check whether RL >= G
                if rlo.geq(self):
                    # R is reversible through RL, replace with RL's Right options
                    change = rev = True
                    reprev.right_options.extend([rlr.clone() for rlr in rlo.right_options])
            if not rev:
                # Right option was not reversible, leave it intact
                reprev.right_options.append(ro.clone())

        # Return the game without reversible options
        if return_change:
            return reprev, change
        return reprev

    # Canonical form
    def canonical_form(self):
        canon = Game()
        # Compute the canonical form of all Left and Right options
        canon.left_options = [lo.canonical_form() for lo in self.left_options]
        canon.right_options = [ro.canonical_form() for ro in self.right_options]
        # Replace reversible options
        change = True
        while change:
            canon, change = canon.replace_reversible(return_change=True)
        # Remove dominated options
        change = True
        while change:
            canon, change = canon.remove_dominated(return_change=True)
        # Return the canonical form
        return canon

    def left_incentive(self, option):
        """Compute a Left incentive.
        The Left incentive is defined as G^L - G.

        Parameters
        ----------
        option : Game or int
            The Left option or its index.

        Returns
        -------
        incentive : Game
            The incentive.

        Notes
        -----
        See Siegel, p. 62, Definition 1.29.
        """
        if isinstance(option, int):
            return self.left_options[option] - self
        return option - self

    def left_incentives(self):
        """Generate all Left incentives.

        Yields
        ------
        incentive : Game
            The Left incentives.
        """
        for gl in self.left_options:
            yield self.left_incentive(gl)

    def right_incentive(self, option):
        """Compute a Right incentive.
        The Right incentive is defined as G^L - G.

        Parameters
        ----------
        option : Game or int
            The Right option or its index.

        Returns
        -------
        incentive : Game
            The incentive.

        Notes
        -----
        See Siegel, p. 62, Definition 1.29.
        """
        if isinstance(option, int):
            return self - self.right_options[option]
        return self - option

    def right_incentives(self):
        """Generate all Right incentives.

        Yields
        ------
        incentive : Game
            The Right incentives.
        """
        for gr in self.right_options:
            yield self.right_incentive(gr)

    def is_integer(self):
        """Whether the game is an integer or not.
        A game is *not* an integer when it has both a Left and Right incentive > -1.

        Returns
        -------
        int_type : bool
            :py:const:`True` when the game is an integer, :py:const:`False` otherwise.

        Notes
        -----
        See Siegel, p. 80, Theorem 3.27.
        """
        return not any(
            left_incentive.gtr(Game("-1")) for left_incentive in self.left_incentives()
        ) or not any(right_incentive.gtr(Game("-1")) for right_incentive in self.right_incentives())

    def integer_value(self):
        """Compute the game's integer value.

        Returns
        -------
        value
            The integer value.

        Raises
        ------
        ValueError
            When the game is not an integer.
        """
        if not self.is_integer():
            raise ValueError("Game is not an integer.")

        value = 0
        cpy = self.clone()
        if self.geq_zero():
            # Game is >= 0
            while cpy.gtr_zero():
                cpy = (cpy + Game("-1")).canonical_form()
                value += 1
            return value
        else:
            # Game is < 0
            while cpy.lss_zero():
                cpy = (cpy + Game("1")).canonical_form()
                value -= 1
            return value

    def norton(self, other):
        """Compute the Norton product of the game with another game.

        The Norton product of G by U is given by:
            n * U, if G is equal to an integer n;
            {G^L*U+U+D|G^R*U-U-D}, otherwise,
        where D ranges over all Left and Right incentives of U.

        Parameters
        ----------
        other : Game
            The game to compute the Norton product with.

        Returns
        -------
        norton : Game
            The computed Norton product.

        Notes
        -----
        See Siegel, p. 150, Exercise 7.15.
        """
        norton = Game()
        if self.is_integer():
            n = self.integer_value()
            # G is an integer -> return n copies of `other`
            if n >= 0:
                for i in range(n):
                    norton = (norton + other).canonical_form()
                return norton
            else:
                for i in range(-n):
                    norton = (norton + other).canonical_form()
                return -norton

        # Not an integer, compute {G^L*U+U+D|G^R*U-U-D}
        # Loop all incentives
        for inc in list(self.left_incentives()) + list(self.right_incentives()):
            # Loop all G^L
            for left_option in self.left_options:
                # Compute G^L*U+U+D
                norton.left_options.append(left_option.norton(other) + other + inc)
            # Loop all G^R
            for right_option in self.left_options:
                # Compute G^R*U-U-D
                norton.right_options.append(right_option.norton(other) - other - inc)
        return norton
