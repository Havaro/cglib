import unittest
from cg.clobber import Clobber


class TestClobber(unittest.TestCase):
    def test_board___get__(self):
        self.assertEqual(Clobber("_").board, "_")
        self.assertEqual(Clobber("L").board, "L")
        self.assertEqual(Clobber("R").board, "R")
        self.assertEqual(Clobber("LR").board, "LR")
        self.assertEqual(Clobber("_|_").board, "_|_")
        self.assertEqual(Clobber("L|L").board, "L|L")
        self.assertEqual(Clobber("R|R").board, "R|R")
        self.assertEqual(Clobber("LR|LR").board, "LR|LR")

    def test_board___set__(self):
        c = Clobber()
        c.board = "LLR"
        self.assertEqual(c.board, "LLR")
        c.board = "LRR"
        self.assertEqual(c.board, "LRR")

        # Test invalid characters
        with self.assertRaises(ValueError):
            c.board = "xyz"

        # Test row length
        with self.assertRaises(ValueError):
            c.board = "L|"
        with self.assertRaises(ValueError):
            c.board = "L|RR"

    def test_rows___get__(self):
        self.assertEqual(Clobber().rows, 0)
        self.assertEqual(Clobber("L").rows, 1)
        self.assertEqual(Clobber("LL").rows, 1)
        self.assertEqual(Clobber("L|L").rows, 2)

    def test_columns___get__(self):
        self.assertEqual(Clobber().columns, 0)
        self.assertEqual(Clobber("L").columns, 1)
        self.assertEqual(Clobber("LL").columns, 2)
        self.assertEqual(Clobber("L|L").columns, 1)

    def test_clone(self):
        # Check values
        self.assertEqual(Clobber("L").clone(), Clobber("L"))
        self.assertEqual(Clobber("_").clone(), Clobber("_"))
        self.assertEqual(Clobber("LR").clone(), Clobber("LR"))
        self.assertEqual(Clobber("LLR").clone(), Clobber("LLR"))
        self.assertEqual(Clobber("RLL").clone(), Clobber("RLL"))

        # Check boards
        self.assertEqual(Clobber("L").clone().board, "L")
        self.assertEqual(Clobber("_").clone().board, "_")
        self.assertEqual(Clobber("LR").clone().board, "LR")
        self.assertEqual(Clobber("LLR").clone().board, "LLR")
        self.assertEqual(Clobber("RLL").clone().board, "RLL")

    def test_inverse(self):
        # Check values
        self.assertEqual(Clobber("L").inverse(), Clobber("R"))
        self.assertEqual(Clobber("_").inverse(), Clobber("_"))
        self.assertEqual(Clobber("LR").inverse(), Clobber("RL"))
        self.assertEqual(Clobber("LLR").inverse(), Clobber("RRL"))
        self.assertEqual(Clobber("RLL").inverse(), Clobber("LRR"))

        # Check boards
        self.assertEqual(Clobber("L").inverse().board, "R")
        self.assertEqual(Clobber("_").inverse().board, "_")
        self.assertEqual(Clobber("LR").inverse().board, "RL")
        self.assertEqual(Clobber("LLR").inverse().board, "RRL")
        self.assertEqual(Clobber("RLL").inverse().board, "LRR")

    def test_sum(self):
        # Check values
        self.assertEqual(Clobber("_").add(Clobber("LLR")), Clobber("LLR"))
        self.assertEqual(Clobber("LRR").add(Clobber("LLR")), Clobber())

        # Check boards
        self.assertEqual(Clobber("_").add(Clobber("LLR")).board, "___|___|LLR")
        self.assertEqual(Clobber("LRR").add(Clobber("LLR")).board, "LRR|___|LLR")

    def test_board_str(self):
        self.assertEqual(Clobber("_").board_str(colsep="", rowsep=""), "_")
        self.assertEqual(Clobber("L").board_str(colsep="", rowsep=""), "L")
        self.assertEqual(Clobber("R").board_str(colsep="", rowsep=""), "R")
        self.assertEqual(Clobber("LR").board_str(colsep="", rowsep=""), "LR")
        self.assertEqual(Clobber("_|_").board_str(colsep="", rowsep=""), "__")
        self.assertEqual(Clobber("L|L").board_str(colsep="", rowsep=""), "LL")
        self.assertEqual(Clobber("R|R").board_str(colsep="", rowsep=""), "RR")
        self.assertEqual(Clobber("LR|LR").board_str(colsep="", rowsep=""), "LRLR")

        self.assertEqual(Clobber("_").board_str(colsep=",", rowsep=""), "_")
        self.assertEqual(Clobber("L").board_str(colsep=",", rowsep=""), "L")
        self.assertEqual(Clobber("R").board_str(colsep=",", rowsep=""), "R")
        self.assertEqual(Clobber("LR").board_str(colsep=",", rowsep=""), "L,R")
        self.assertEqual(Clobber("_|_").board_str(colsep=",", rowsep=""), "__")
        self.assertEqual(Clobber("L|L").board_str(colsep=",", rowsep=""), "LL")
        self.assertEqual(Clobber("R|R").board_str(colsep=",", rowsep=""), "RR")
        self.assertEqual(Clobber("LR|LR").board_str(colsep=",", rowsep=""), "L,RL,R")

        self.assertEqual(Clobber("_").board_str(colsep="", rowsep=";"), "_")
        self.assertEqual(Clobber("L").board_str(colsep="", rowsep=";"), "L")
        self.assertEqual(Clobber("R").board_str(colsep="", rowsep=";"), "R")
        self.assertEqual(Clobber("LR").board_str(colsep="", rowsep=";"), "LR")
        self.assertEqual(Clobber("_|_").board_str(colsep="", rowsep=";"), "_;_")
        self.assertEqual(Clobber("L|L").board_str(colsep="", rowsep=";"), "L;L")
        self.assertEqual(Clobber("R|R").board_str(colsep="", rowsep=";"), "R;R")
        self.assertEqual(Clobber("LR|LR").board_str(colsep="", rowsep=";"), "LR;LR")

        self.assertEqual(Clobber("_").board_str(colsep=",", rowsep=";"), "_")
        self.assertEqual(Clobber("L").board_str(colsep=",", rowsep=";"), "L")
        self.assertEqual(Clobber("R").board_str(colsep=",", rowsep=";"), "R")
        self.assertEqual(Clobber("LR").board_str(colsep=",", rowsep=";"), "L,R")
        self.assertEqual(Clobber("_|_").board_str(colsep=",", rowsep=";"), "_;_")
        self.assertEqual(Clobber("L|L").board_str(colsep=",", rowsep=";"), "L;L")
        self.assertEqual(Clobber("R|R").board_str(colsep=",", rowsep=";"), "R;R")
        self.assertEqual(Clobber("LR|LR").board_str(colsep=",", rowsep=";"), "L,R;L,R")

    def test_moves(self):
        c = Clobber()  # Empty games
        with self.assertRaises(StopIteration):
            next(c.moves("L"))
        with self.assertRaises(StopIteration):
            next(c.moves("R"))

        c = Clobber("LR")  # Star game
        self.assertTrue(Clobber(next(c.moves("L"))).equal_zero())
        self.assertTrue(Clobber(next(c.moves("R"))).equal_zero())
        c = Clobber("LR")
        self.assertEqual(next(c.moves("L")), "_L")
        self.assertEqual(next(c.moves("R")), "R_")
        c = Clobber("LLR")  # Up game
        self.assertTrue(Clobber(next(c.moves("L"))).equal_zero())
        self.assertEqual(Clobber(next(c.moves("R"))), Clobber("LR"))
        c = Clobber("LLR")
        self.assertEqual(next(c.moves("L")), "L_L")
        self.assertEqual(next(c.moves("R")), "LR_")
        c = Clobber("LRR")  # Down game
        self.assertEqual(Clobber(next(c.moves("L"))), Clobber("LR"))
        self.assertTrue(Clobber(next(c.moves("R"))).equal_zero())
        c = Clobber("LRR")
        self.assertEqual(next(c.moves("L")), "_LR")
        self.assertEqual(next(c.moves("R")), "R_R")
