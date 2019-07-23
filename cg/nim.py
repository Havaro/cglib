from cg.game import Game


class Nim(Game):
    """
    Attributes
    ----------
    board
    rows
    columns
    """

    def __init__(self, board=""):
        self.board = board
        self.left_options = [Nim(b) for b in self.moves()]
        self.right_options = [Nim(b) for b in self.moves()]

    @property
    def board(self):
        return self.board_str(colsep="", rowsep="|")

    @board.setter
    def board(self, value):
        # Check for invalid characters
        for c in value:
            if c not in "+|":
                raise ValueError("Board can only contain '+|' characters.")

        self._board = value.split("|") if value else []

    @property
    def rows(self):
        """int: Number of rows of the board."""
        return len(self._board)

    def clone(self):
        """Clone a Nim game.

        Returns
        -------
        clone : Nim
            A deep copy of the Nim game.
        """
        clone = Nim()
        clone._board = self._board.copy()
        clone.left_options = [option.clone() for option in self.left_options]
        clone.right_options = [option.clone() for option in self.right_options]
        return clone

    def inverse(self):
        """Inverse a Nim game.
        All options for Left are swapped with those of Right recursively.

        Returns
        -------
        inverse : Nim
            The inverse Nim game.
        """
        # The inverse of a Nim game is just itself
        return self.clone()

    def add(self, other):
        """Add a Nim game.

        Returns
        -------
        summed : Nim
            The summed Nim game.
        """
        summed = Nim()

        # Add rows of other to self
        summed._board = self._board + other._board

        # Add all options
        left_self = [slo.add(other) for slo in self.left_options]
        left_other = [self.add(olo) for olo in other.left_options]
        summed.left_options = left_self + left_other
        right_self = [sro.add(other) for sro in self.right_options]
        right_other = [self.add(oro) for oro in other.right_options]
        summed.right_options = right_self + right_other
        return summed

    def board_str(self, colsep="", rowsep="\n"):
        """Return the board as :py:class:`str`.

        Parameters
        ----------
        colsep : str, optional
            The string to separate columns. Defaults to ''.

        rowsep : str, optional
            The string to separate rows. Defaults to '\n'.

        Returns
        -------
        board : str
            The board in string format.
        """
        return rowsep.join(colsep.join(r) for r in self._board)

    def moves(self):
        """Generate the moves a player can do.

        Yields
        ------
        move : str
            The board string of a move.
        """
        # In Nim, both players have the same moves
        for i in range(self.rows):
            for j in range(len(self._board[i])):
                optboard = self._board.copy()
                # Remove all pieces above j
                optboard[i] = optboard[i][:j]
                yield "|".join(optboard)
