from cg.game import Game


class Clobber(Game):
    """
    Attributes
    ----------
    board
    rows
    columns
    """

    def __init__(self, board=""):
        self.board = board
        self.left_options = [Clobber(b) for b in self.moves("L")]
        self.right_options = [Clobber(b) for b in self.moves("R")]

    @property
    def board(self):
        return self.board_str(colsep="", rowsep="|")

    @board.setter
    def board(self, value):
        # Check for invalid characters
        for c in value:
            if c not in "_LR|":
                raise ValueError("Board can only contain '_LR|' characters.")

        # Assert that all rows are the same length
        rows = value.split("|")
        n = len(rows[0])
        if not all(len(row) == n for row in rows):
            raise ValueError("All rows must be the same length.")

        self._board = rows if n else []

    @property
    def rows(self):
        """int: Number of rows of the board."""
        return len(self._board)

    @property
    def columns(self):
        """int: Number of columns of the board."""
        return len(self._board[0]) if self._board else 0

    def clone(self):
        """Clone a Clobber game.

        Returns
        -------
        clone : Clobber
            A deep copy of the Clobber game.
        """
        clone = Clobber()
        clone._board = self._board.copy()
        clone.left_options = [option.clone() for option in self.left_options]
        clone.right_options = [option.clone() for option in self.right_options]
        return clone

    def inverse(self):
        """Inverse a Clobber game.
        All options for Left are swapped with those of Right recursively.

        Returns
        -------
        inverse : Clobber
            The inverse Clobber game.
        """
        inverse = self.clone()
        # Swap colors on the board
        inverse._board = [row.replace("L", "T") for row in inverse._board]
        inverse._board = [row.replace("R", "L") for row in inverse._board]
        inverse._board = [row.replace("T", "R") for row in inverse._board]
        # Swap Left and Right options
        inverse.left_options, inverse.right_options = inverse.right_options, inverse.left_options
        # Invert all options
        inverse.left_options = [lo.inverse() for lo in inverse.left_options]
        inverse.right_options = [ro.inverse() for ro in inverse.right_options]
        return inverse

    def add(self, other):
        """Add a Clobber game.

        Returns
        -------
        summed : Clobber
            The summed Clobber game.
        """
        summed = Clobber()

        # Add rows of other to self
        summed._board = [row.ljust(other.columns, "_") for row in self._board]
        summed._board.append("_" * len(summed._board[0]))
        summed._board += [row.ljust(self.columns, "_") for row in other._board]

        # Add all options
        left_self = [slo.add(other) for slo in self.left_options]
        left_other = [self.add(olo) for olo in other.left_options]
        summed.left_options = left_self + left_other
        right_self = [sro.add(other) for sro in self.right_options]
        right_other = [self.add(oro) for oro in other.right_options]
        summed.right_options = right_self + right_other
        return summed

    def board_str(self, colsep=" ", rowsep="\n"):
        """Return the board as :py:class:`str`.

        Parameters
        ----------
        colsep : str, optional
            The string to separate columns. Defaults to ' '.

        rowsep : str, optional
            The string to separate rows. Defaults to '\n'.

        Returns
        -------
        board : str
            The board in string format.
        """
        return rowsep.join(colsep.join(r) for r in self._board)

    def moves(self, player):
        """Generate the moves a player can do.

        Parameters
        ----------
        player : {"L", "R"}
            The player to generate the moves of.

        Yields
        ------
        move : str
            The board string of a move.
        """
        for i in range(self.rows):
            for j in range(self.columns):
                if self._board[i][j] == player:
                    # Move by going up
                    if (
                        i > 0
                        and self._board[i - 1][j] != self._board[i][j]
                        and self._board[i - 1][j] != "_"
                    ):
                        optboard = self._board.copy()
                        srow = list(self._board[i])
                        srow[j] = "_"
                        optboard[i] = "".join(srow)
                        trow = list(self._board[i - 1])
                        trow[j] = player
                        optboard[i - 1] = "".join(trow)
                        yield "|".join("".join(r) for r in optboard)

                    # Move by going left
                    if (
                        j > 0
                        and self._board[i][j - 1] != self._board[i][j]
                        and self._board[i][j - 1] != "_"
                    ):
                        optboard = self._board.copy()
                        row = list(self._board[i])
                        row[j] = "_"
                        row[j - 1] = player
                        optboard[i] = "".join(row)
                        yield "|".join("".join(r) for r in optboard)

                    # Move by going right
                    if (
                        j < self.columns - 1
                        and self._board[i][j + 1] != self._board[i][j]
                        and self._board[i][j + 1] != "_"
                    ):
                        optboard = self._board.copy()
                        row = list(self._board[i])
                        row[j] = "_"
                        row[j + 1] = player
                        optboard[i] = "".join(row)
                        yield "|".join("".join(r) for r in optboard)

                    # Move by going down
                    if (
                        i < self.rows - 1
                        and self._board[i + 1][j] != self._board[i][j]
                        and self._board[i + 1][j] != "_"
                    ):
                        optboard = self._board.copy()
                        srow = list(self._board[i])
                        srow[j] = "_"
                        optboard[i] = "".join(srow)
                        trow = list(self._board[i + 1])
                        trow[j] = player
                        optboard[i + 1] = "".join(trow)
                        yield "|".join("".join(r) for r in optboard)
