import unittest
from cg.game import Game


class TestGame(unittest.TestCase):
    def test_str(self):
        g = Game()
        self.assertEqual(str(g), "0")
        g.left_options.append(Game())
        self.assertEqual(str(g), "1")
        g.right_options.append(Game())
        self.assertEqual(str(g), "*")
        g.left_options.clear()
        self.assertEqual(str(g), "-1")

    def test_repr(self):
        g = Game()
        self.assertEqual(g.__repr__(), "0")
        g.left_options.append(Game())
        self.assertEqual(g.__repr__(), "1")
        g.right_options.append(Game())
        self.assertEqual(g.__repr__(), "*")
        g.left_options.clear()
        self.assertEqual(g.__repr__(), "-1")

    def test_clear(self):
        g = Game()
        g.left_options.append(Game())
        g.right_options.append(Game())
        g.clear()
        self.assertFalse(g.left_options)
        self.assertFalse(g.right_options)

    def test_set_node_cgn(self):
        g = Game()
        num = g._set_node_cgn("{|}", 1)
        self.assertEqual(str(g), "0")
        self.assertEqual(num, 2)
        num = g._set_node_cgn("{|{|}}", 3)
        self.assertEqual(str(g), "0")
        self.assertEqual(num, 4)
        num = g._set_node_cgn("{{|}|{|}}", 1)
        self.assertEqual(str(g), "*")
        self.assertEqual(num, 8)

    def test_set_cgn(self):
        g = Game().set_cgn("0")
        self.assertEqual(str(g), "0")
        with self.assertRaises(ValueError):
            Game().set_cgn("abc")

    def test_get_node_cgn(self):
        g = Game()
        self.assertEqual(g._get_node_cgn(), "0")
        g.left_options.append(Game())
        self.assertEqual(g._get_node_cgn(), "1")
        g.right_options.append(Game())
        self.assertEqual(g._get_node_cgn(), "*")
        g.left_options.clear()
        self.assertEqual(g._get_node_cgn(), "-1")

    def test_get_cgn(self):
        g = Game()
        self.assertEqual(g.get_cgn(), "0")
        g.left_options.append(Game())
        self.assertEqual(g.get_cgn(), "1")
        g.right_options.append(Game())
        self.assertEqual(g.get_cgn(), "*")
        g.left_options.clear()
        self.assertEqual(g.get_cgn(), "-1")

    def test_get_node_cgn_dot(self):
        dot_str, num = Game()._get_node_cgn_dot("", 0)
        target_str = '\t0[label="0"];\n'
        self.assertEqual(dot_str, target_str)
        self.assertEqual(num, 0)

        dot_str, num = Game("1")._get_node_cgn_dot("abc", 2)
        target_str = 'abc\t2[label="1"];\n\t3[label="0"];\n\t2 -> 3[label="L"];\n'
        self.assertEqual(dot_str, target_str)
        self.assertEqual(num, 3)

        dot_str, num = Game("*2")._get_node_cgn_dot("xyz", -2)
        target_str = 'xyz\t-2[label="*2"];\n\t-1[label="0"];\n\t-2 -> -1[label="L"];\n\t0[label="*"];\n\t1[label="0"];\n\t0 -> 1[label="L"];\n\t2[label="0"];\n\t0 -> 2[label="R"];\n\t-2 -> 0[label="L"];\n\t3[label="0"];\n\t-2 -> 3[label="R"];\n\t4[label="*"];\n\t5[label="0"];\n\t4 -> 5[label="L"];\n\t6[label="0"];\n\t4 -> 6[label="R"];\n\t-2 -> 4[label="R"];\n'
        self.assertEqual(dot_str, target_str)
        self.assertEqual(num, 6)

    def test_get_cgn_dot(self):
        comp_str = Game().get_cgn_dot()
        target_str = 'digraph Game {\n\t0[label="0"];\n}'
        self.assertEqual(comp_str, target_str)

        comp_str = Game("1").get_cgn_dot()
        target_str = 'digraph Game {\n\t0[label="1"];\n\t1[label="0"];\n\t0 -> 1[label="L"];\n}'
        self.assertEqual(comp_str, target_str)

        comp_str = Game("*").get_cgn_dot()
        target_str = 'digraph Game {\n\t0[label="*"];\n\t1[label="0"];\n\t0 -> 1[label="L"];\n\t2[label="0"];\n\t0 -> 2[label="R"];\n}'
        self.assertEqual(comp_str, target_str)

        comp_str = Game("-1").get_cgn_dot()
        target_str = 'digraph Game {\n\t0[label="-1"];\n\t1[label="0"];\n\t0 -> 1[label="R"];\n}'
        self.assertEqual(comp_str, target_str)

        comp_str = Game("*2").get_cgn_dot()
        target_str = 'digraph Game {\n\t0[label="*2"];\n\t1[label="0"];\n\t0 -> 1[label="L"];\n\t2[label="*"];\n\t3[label="0"];\n\t2 -> 3[label="L"];\n\t4[label="0"];\n\t2 -> 4[label="R"];\n\t0 -> 2[label="L"];\n\t5[label="0"];\n\t0 -> 5[label="R"];\n\t6[label="*"];\n\t7[label="0"];\n\t6 -> 7[label="L"];\n\t8[label="0"];\n\t6 -> 8[label="R"];\n\t0 -> 6[label="R"];\n}'
        self.assertEqual(comp_str, target_str)

    def test_left_incentive(self):
        # Check Game parameter
        self.assertEqual(Game("*").left_incentive(Game("0")), Game("*"))
        self.assertEqual(Game("^").left_incentive(Game("0")), Game("v"))
        self.assertEqual(Game("^*").left_incentive(Game("*")), Game("v"))
        self.assertEqual(Game("v").left_incentive(Game("*")), Game("^*"))

        # Check int parameter
        self.assertEqual(Game("*").left_incentive(0), Game("*"))
        self.assertEqual(Game("^").left_incentive(0), Game("v"))
        self.assertEqual(Game("^*").left_incentive(1), Game("v"))
        self.assertEqual(Game("v").left_incentive(-1), Game("^*"))

    def test_left_incentives(self):
        # Check generator length
        self.assertEqual(len(list(Game("0").left_incentives())), 0)
        self.assertEqual(len(list(Game("*").left_incentives())), 1)
        self.assertEqual(len(list(Game("^").left_incentives())), 1)
        self.assertEqual(len(list(Game("^*").left_incentives())), 2)

        # Check generator values
        self.assertListEqual(list(Game("0").left_incentives()), [])
        self.assertListEqual(list(Game("*").left_incentives()), [Game("*")])
        self.assertListEqual(list(Game("^").left_incentives()), [Game("v")])
        self.assertListEqual(list(Game("^*").left_incentives()), [Game("v*"), Game("v")])

    def test_right_incentive(self):
        # Check Game parameter
        self.assertEqual(Game("*").right_incentive(Game("0")), Game("*"))
        self.assertEqual(Game("^").right_incentive(Game("*")), Game("^*"))
        self.assertEqual(Game("^*").right_incentive(Game("*")), Game("^"))
        self.assertEqual(Game("v").right_incentive(Game("*")), Game("v*"))

        # Check int parameter
        self.assertEqual(Game("*").right_incentive(0), Game("*"))
        self.assertEqual(Game("^").right_incentive(0), Game("^*"))
        self.assertEqual(Game("v*").right_incentive(1), Game("v"))
        self.assertEqual(Game("v").right_incentive(-1), Game("v"))

    def test_right_incentives(self):
        # Check generator length
        self.assertEqual(len(list(Game("0").right_incentives())), 0)
        self.assertEqual(len(list(Game("*").right_incentives())), 1)
        self.assertEqual(len(list(Game("v").right_incentives())), 1)
        self.assertEqual(len(list(Game("v*").right_incentives())), 2)

        # Check generator values
        self.assertListEqual(list(Game("0").right_incentives()), [])
        self.assertListEqual(list(Game("*").right_incentives()), [Game("*")])
        self.assertListEqual(list(Game("v").right_incentives()), [Game("v")])
        self.assertListEqual(list(Game("v*").right_incentives()), [Game("v*"), Game("v")])

    def test_is_integer(self):
        # Check integer games
        self.assertTrue(Game("-3").is_integer())
        self.assertTrue(Game("-1").is_integer())
        self.assertTrue(Game("-2").is_integer())
        self.assertTrue(Game("0").is_integer())
        self.assertTrue(Game("1").is_integer())
        self.assertTrue(Game("2").is_integer())
        self.assertTrue(Game("3").is_integer())
        self.assertTrue(Game("{-1|1}").is_integer())

        # Check non-integer games
        self.assertFalse(Game("*").is_integer())
        self.assertFalse(Game("^").is_integer())
        self.assertFalse(Game("v").is_integer())
        self.assertFalse(Game("{1|-1}").is_integer())

    def test_integer_value(self):
        # Check integer games
        self.assertEqual(Game("-3").integer_value(), -3)
        self.assertEqual(Game("-1").integer_value(), -1)
        self.assertEqual(Game("-2").integer_value(), -2)
        self.assertEqual(Game("0").integer_value(), 0)
        self.assertEqual(Game("1").integer_value(), 1)
        self.assertEqual(Game("2").integer_value(), 2)
        self.assertEqual(Game("3").integer_value(), 3)

        # Check ValueError on non-integer games
        with self.assertRaises(ValueError):
            Game("*").integer_value()
        with self.assertRaises(ValueError):
            Game("^").integer_value()
        with self.assertRaises(ValueError):
            Game("v").integer_value()

    def test_norton(self):
        # Integer times non-integer
        self.assertEqual(Game("-2").norton(Game("^")), Game("v") + Game("v"))
        self.assertEqual(Game("-1").norton(Game("^")), Game("v"))
        self.assertEqual(Game("0").norton(Game("^")), Game("0"))
        self.assertEqual(Game("1").norton(Game("^")), Game("^"))
        self.assertEqual(Game("2").norton(Game("^")), Game("^") + Game("^"))

        # Non-integer times other game
        self.assertEqual(Game("*").norton(Game("*")), Game("*"))
        self.assertEqual(Game("*").norton(Game("^")), Game("0"))
        self.assertEqual(Game("^").norton(Game("v")), Game("0"))
        self.assertEqual(Game("^").norton(Game("*")), Game("*"))
        self.assertEqual(Game("v").norton(Game("0")), Game("0"))

    def test_geq_zero(self):
        self.assertTrue(Game("0").geq_zero())
        self.assertTrue(Game("1").geq_zero())
        self.assertTrue(Game("^").geq_zero())

        self.assertFalse(Game("*").geq_zero())
        self.assertFalse(Game("-1").geq_zero())
        self.assertFalse(Game("v").geq_zero())

    def test_leq_zero(self):
        self.assertTrue(Game("0").leq_zero())
        self.assertTrue(Game("-1").leq_zero())
        self.assertTrue(Game("v").leq_zero())

        self.assertFalse(Game("*").leq_zero())
        self.assertFalse(Game("1").leq_zero())
        self.assertFalse(Game("^").leq_zero())

    def test_lin_zero(self):
        self.assertTrue(Game("*").lin_zero())
        self.assertTrue(Game("-1").lin_zero())
        self.assertTrue(Game("v").lin_zero())

        self.assertFalse(Game("0").lin_zero())
        self.assertFalse(Game("1").lin_zero())
        self.assertFalse(Game("^").lin_zero())

    def test_gin_zero(self):
        self.assertTrue(Game("*").gin_zero())
        self.assertTrue(Game("1").gin_zero())
        self.assertTrue(Game("^").gin_zero())

        self.assertFalse(Game("0").gin_zero())
        self.assertFalse(Game("-1").gin_zero())
        self.assertFalse(Game("v").gin_zero())

    def test_gtr_zero(self):
        self.assertTrue(Game("1").gtr_zero())
        self.assertTrue(Game("^").gtr_zero())

        self.assertFalse(Game("0").gtr_zero())
        self.assertFalse(Game("*").gtr_zero())
        self.assertFalse(Game("v").gtr_zero())
        self.assertFalse(Game("-1").gtr_zero())

    def test_lss_zero(self):
        self.assertTrue(Game("v").lss_zero())
        self.assertTrue(Game("-1").lss_zero())

        self.assertFalse(Game("1").lss_zero())
        self.assertFalse(Game("^").lss_zero())
        self.assertFalse(Game("0").lss_zero())
        self.assertFalse(Game("*").lss_zero())

    def test_equal_zero(self):
        self.assertTrue(Game("0").equal_zero())

        self.assertFalse(Game("1").equal_zero())
        self.assertFalse(Game("^").equal_zero())
        self.assertFalse(Game("*").equal_zero())
        self.assertFalse(Game("v").equal_zero())
        self.assertFalse(Game("-1").equal_zero())

    def test_incomparable_zero(self):
        self.assertTrue(Game("*").incomparable_zero())

        self.assertFalse(Game("1").incomparable_zero())
        self.assertFalse(Game("^").incomparable_zero())
        self.assertFalse(Game("0").incomparable_zero())
        self.assertFalse(Game("v").incomparable_zero())
        self.assertFalse(Game("-1").incomparable_zero())

    def test_inverse(self):
        self.assertEqual(Game("1").inverse(), Game("-1"))
        self.assertEqual(Game("0").inverse(), Game("0"))
        self.assertEqual(Game("*").inverse(), Game("*"))
        self.assertEqual(Game("^").inverse(), Game("v"))
        self.assertEqual(Game("v").inverse(), Game("^"))
        self.assertEqual(Game("{^|}").inverse(), Game("{|v}"))
        self.assertEqual(Game("{v|}").inverse(), Game("{|^}"))
        self.assertEqual(Game("{|^}").inverse(), Game("{v|}"))
        self.assertEqual(Game("{|v}").inverse(), Game("{^|}"))

    def test_add(self):
        self.assertEqual(Game("0").add(Game("1")), Game("1"))
        self.assertEqual(Game("-1").add(Game("1")), Game("0"))

    def test_subtract(self):
        g = Game("0").subtract(Game("1"))
        self.assertEqual(g, Game("-1"))
        g = Game("1").subtract(Game("1"))
        self.assertEqual(g, Game("{-1|1}"))
        g = Game("-1").subtract(Game("-1"))
        self.assertEqual(g, Game("{-1|1}"))
        g = Game("1").subtract(Game("0"))
        self.assertEqual(g, Game("1"))
        g = Game("*").subtract(Game("*"))
        self.assertEqual(g, Game("{*,*|*,*}"))
        g = Game("^").subtract(Game("v"))
        self.assertEqual(g, Game("{^,^|{*,^|^,{*,*|*,*}},{*,^|^,{*,*|*,*}}}"))

    def test___eq__(self):
        self.assertTrue(Game("0") == Game("0"))
        self.assertTrue(Game("1") == Game("1"))
        self.assertTrue(Game("1") - Game("1") == Game("0"))
        self.assertTrue(Game("*") == Game("*").inverse())

    def test___add__(self):
        self.assertEqual(Game("0") + Game("1"), Game("1"))
        self.assertEqual(Game("-1") + Game("1"), Game("0"))

    def test___sub__(self):
        g = Game("0") - Game("1")
        self.assertEqual(g, Game("-1"))
        g = Game("1") - Game("1")
        self.assertEqual(g, Game("{-1|1}"))
        g = Game("-1") - Game("-1")
        self.assertEqual(g, Game("{-1|1}"))
        g = Game("1") - Game("0")
        self.assertEqual(g, Game("1"))
        g = Game("*") - Game("*")
        self.assertEqual(g, Game("{*,*|*,*}"))
        g = Game("^") - Game("v")
        self.assertEqual(g, Game("{^,^|{*,^|^,{*,*|*,*}},{*,^|^,{*,*|*,*}}}"))

    def test___neg__(self):
        self.assertEqual(-Game("1"), Game("-1"))
        self.assertEqual(-Game("0"), Game("0"))
        self.assertEqual(-Game("*"), Game("*"))
        self.assertEqual(-Game("^"), Game("v"))
        self.assertEqual(-Game("v"), Game("^"))
        self.assertEqual(-Game("{^|}"), Game("{|v}"))
        self.assertEqual(-Game("{v|}"), Game("{|^}"))
        self.assertEqual(-Game("{|^}"), Game("{v|}"))
        self.assertEqual(-Game("{|v}"), Game("{^|}"))

    def test_geq(self):
        self.assertTrue(Game().geq(Game()))
        self.assertTrue(Game("1").geq(Game()))
        self.assertTrue(Game().geq(Game("-1")))
        self.assertTrue(Game("^").geq(Game()))
        self.assertTrue(Game("^").geq(Game("v")))
        self.assertTrue(Game("^").geq(Game("-1")))

        self.assertFalse(Game().geq(Game("*")))
        self.assertFalse(Game("v").geq(Game("v*")))
        self.assertFalse(Game("*").geq(Game("*2")))

    def test_leq(self):
        self.assertTrue(Game().leq(Game()))
        self.assertTrue(Game().leq(Game("1")))
        self.assertTrue(Game("-1").leq(Game()))
        self.assertTrue(Game().leq(Game("^")))
        self.assertTrue(Game("v").leq(Game("^")))
        self.assertTrue(Game("-1").leq(Game("^")))

        self.assertFalse(Game("*").leq(Game()))
        self.assertFalse(Game("v*").leq(Game("v")))
        self.assertFalse(Game("*2").leq(Game("*")))

    def test_gin(self):
        self.assertTrue(Game().gin(Game("*")))
        self.assertTrue(Game("v").gin(Game("v*")))
        self.assertTrue(Game("*").gin(Game("*2")))
        self.assertTrue(Game("1").gin(Game()))
        self.assertTrue(Game().gin(Game("-1")))
        self.assertTrue(Game("^").gin(Game()))
        self.assertTrue(Game("^").gin(Game("v")))
        self.assertTrue(Game("^").gin(Game("-1")))

        self.assertFalse(Game().gin(Game()))
        self.assertFalse(Game("1").gin(Game("1")))
        self.assertFalse(Game("-1").gin(Game("1")))
        self.assertFalse(Game("v").gin(Game("^")))

    def test_lin(self):
        self.assertTrue(Game("*").lin(Game()))
        self.assertTrue(Game("v*").lin(Game("v")))
        self.assertTrue(Game("*2").lin(Game("*")))
        self.assertTrue(Game().lin(Game("1")))
        self.assertTrue(Game("-1").lin(Game()))
        self.assertTrue(Game().lin(Game("^")))
        self.assertTrue(Game("v").lin(Game("^")))
        self.assertTrue(Game("-1").lin(Game("^")))

        self.assertFalse(Game().lin(Game()))
        self.assertFalse(Game("1").lin(Game("1")))
        self.assertFalse(Game("1").lin(Game("-1")))
        self.assertFalse(Game("^").lin(Game("v")))

    def test_gtr(self):
        self.assertTrue(Game("1").gtr(Game()))
        self.assertTrue(Game().gtr(Game("-1")))
        self.assertTrue(Game("^").gtr(Game()))
        self.assertTrue(Game("^").gtr(Game("v")))
        self.assertTrue(Game("^").gtr(Game("-1")))

        self.assertFalse(Game().gtr(Game()))
        self.assertFalse(Game().gtr(Game("*")))
        self.assertFalse(Game("*").gtr(Game("*")))
        self.assertFalse(Game("v").gtr(Game("v*")))
        self.assertFalse(Game("*").gtr(Game("*2")))

    def test_lss(self):
        self.assertTrue(Game().lss(Game("1")))
        self.assertTrue(Game("-1").lss(Game()))
        self.assertTrue(Game().lss(Game("^")))
        self.assertTrue(Game("v").lss(Game("^")))
        self.assertTrue(Game("-1").lss(Game("^")))

        self.assertFalse(Game().lss(Game()))
        self.assertFalse(Game("*").lss(Game()))
        self.assertFalse(Game("*").lss(Game("*")))
        self.assertFalse(Game("v*").lss(Game("v")))
        self.assertFalse(Game("*2").lss(Game("*")))

    def test_equal(self):
        self.assertTrue(Game("0").equal(Game("0")))
        self.assertTrue(Game("1").equal(Game("1")))
        self.assertTrue((Game("1") - Game("1")).equal(Game("0")))
        self.assertTrue(Game("*").equal(Game("*").inverse()))

    def test_incomparable(self):
        self.assertTrue(Game("0").incomparable(Game("*")))
        self.assertTrue(Game("1").incomparable(Game("1") + Game("*")))
        self.assertTrue((Game("1") - Game("1")).incomparable(Game("*")))
        self.assertTrue(Game("*").incomparable(Game("0").inverse()))

    def test_outcome_class(self):
        # First player win
        self.assertEqual(Game("*").outcome_class(), "N")
        self.assertEqual(Game("*2").outcome_class(), "N")
        self.assertEqual(Game("{^|v}").outcome_class(), "N")

        # Second player win
        self.assertEqual(Game().outcome_class(), "P")
        self.assertEqual(Game("0").outcome_class(), "P")
        self.assertEqual(Game("{*|*}").outcome_class(), "P")

        # Win for Left
        self.assertEqual(Game("1").outcome_class(), "L")
        self.assertEqual(Game("^").outcome_class(), "L")
        self.assertEqual(Game("{1|^}").outcome_class(), "L")

        # Win for Right
        self.assertEqual(Game("-1").outcome_class(), "R")
        self.assertEqual(Game("v").outcome_class(), "R")
        self.assertEqual(Game("{-1|v}").outcome_class(), "R")

    def test_companion(self):
        # First player win
        self.assertEqual(str(Game("*").companion()), "{*|*}")
        self.assertEqual(str(Game("*2").companion()), "{*,{*|*}|*,{*|*}}")
        self.assertEqual(str(Game("{^|v}").companion()), "{{*,0|{*|*}}|{{*|*}|*,0}}")

        # Second player win
        self.assertEqual(str(Game().companion()), "*")
        self.assertEqual(str(Game("0").companion()), "*")
        self.assertEqual(str(Game("{*|*}").companion()), "*")

        # Win for Left
        self.assertEqual(str(Game("1").companion()), "{*,0|}")
        self.assertEqual(str(Game("^").companion()), "{*,0|{*|*}}")
        self.assertEqual(str(Game("{1|^}").companion()), "{0,{*,0|}|{*,0|{*|*}}}")

        # Win for Right
        self.assertEqual(str(Game("-1").companion()), "{|*,0}")
        self.assertEqual(str(Game("v").companion()), "{{*|*}|*,0}")
        self.assertEqual(str(Game("{-1|v}").companion()), "{{|*,0}|0,{{*|*}|*,0}}")

    def test_remove_dominated(self):
        # With return_change = False
        g = Game("{0,1|0,1}").remove_dominated()
        self.assertEqual(g, Game("{1|0}"))
        g = Game("{*,0|-1,*,1}").remove_dominated()
        self.assertEqual(g, Game("{*,0|-1}"))
        g = Game("{0,*,-1,*|-1,0,-1}").remove_dominated()
        self.assertEqual(g, Game("{*,0|-1}"))

        # With return_change = True
        g, c = Game("{0,1|0,1}").remove_dominated(return_change=True)
        self.assertEqual(g, Game("{1|0}"))
        self.assertTrue(c)
        g, c = Game("{*,0|-1,*,1}").remove_dominated(return_change=True)
        self.assertEqual(g, Game("{*,0|-1}"))
        self.assertTrue(c)
        g, c = Game("{0,*,-1,*|-1,0,-1}").remove_dominated(return_change=True)
        self.assertEqual(g, Game("{*,0|-1}"))
        self.assertTrue(c)
        g, c = Game().remove_dominated(return_change=True)
        self.assertEqual(g, Game())
        self.assertFalse(c)
        g, c = Game("*").remove_dominated(return_change=True)
        self.assertEqual(g, Game("*"))
        self.assertFalse(c)

    def test_replace_reversible(self):
        # With return_change = False
        g = Game("{*|*}").replace_reversible()
        self.assertEqual(g, Game("0"))
        g = Game("{^,*|0}").replace_reversible()
        self.assertEqual(g, Game("^*"))

        # With return_change = True
        g, c = Game("{*|*}").replace_reversible(return_change=True)
        self.assertEqual(g, Game("0"))
        self.assertTrue(c)
        g, c = Game("{^,*|0}").replace_reversible(return_change=True)
        self.assertEqual(g, Game("^*"))
        self.assertTrue(c)
        g, c = Game().replace_reversible(return_change=True)
        self.assertEqual(g, Game())
        self.assertFalse(c)
        g, c = Game("*").replace_reversible(return_change=True)
        self.assertEqual(g, Game("*"))
        self.assertFalse(c)

    def test_canonical_form(self):
        self.assertTrue((Game("*") + Game("*")).canonical_form().equal_zero())
        self.assertEqual(str(Game("{^,*|^,0}").canonical_form()), "^*")
        self.assertEqual(str(Game("^*").canonical_form()), "^*")
        self.assertEqual(str(Game("{2,1,0|-1,-3,2}").canonical_form()), "{{1|}|{|{|-1}}}")
        self.assertEqual(str(Game("*").canonical_form()), "*")
        self.assertEqual(str(Game("{{*,0|{*|*}},{*|*}|*,{*|*,{*|*}}}").canonical_form()), "{0,^*|*,v}")
        self.assertEqual(str(Game("{*2,*3,{0|v*},{^|0,v*}|*,*2,*3,{*,^|0,v*},{0,^*|*,v},{0,^*|0,v*},{^,^*|v,v*}}").canonical_form()), "{0|*,*2,*3,{0,^*|*,v},{0,^*|0,v*}}")
        self.assertEqual(str(Game("{*,0,{*,*2,0|*,0},{*,^|v,v*}|*,*2,*3,{*,^|*,v}}").canonical_form()), "{0|*,*2,*3}")
        self.assertEqual(str(Game("{{*,^|*,0},{0,^*|*,0},{^,^*|0,v*}|*,{0,^*|*,v},{^*|0},{^,^*|v,v*}}").canonical_form()), "{{*,^|*,0},{0,^*|*,0},{^,^*|0,v*}|0}")
        self.assertEqual(str(Game("{{*,*2|0},{*,0|*,*2,0},{^,^*|v,v*}|v,{*,0|*,v},{*,^|v,v*},{^*|v},{^|*,0}}").canonical_form()), "{{*,*2|0},{*,0|*,*2,0},{^,^*|v,v*}|0}")
        self.assertEqual(str(Game("{{*,0|*2,0},{0|v*},{^,^*|*,v}|*2,{0|*,*2},{^,^*|*,*2,0},{^|v*}}").canonical_form()), "{0|*2,{0|*,*2},{^,^*|*,*2,0},{^|v*}}")
        self.assertEqual(str(Game("{{*,0|*,*2,0},{*,0|v},{^*|0}|{*,0|*,v},{*,^|v,v*},{*,v|0},{*2,0|*,0}}").canonical_form()), "{*,{*,0|*,*2,0},{^*|0}|{*,v|0}}")
        self.assertEqual(str(Game("{{*,0|*,*2,0},{*,^|*,v},{0,^*|*,v},{^,^*|0,v*}|0,{*,0|0,^*},{^,^*|*,v}}").canonical_form()), "{{*,0|*,*2,0},{*,^|*,v},{0,^*|*,v},{^,^*|0,v*}|0}")
        self.assertEqual(str(Game("{*,0,{*,^|*,0},{0,^*|*,0},{^,^*|*,v}|*,*2,*3,0,{*,^|0,v*},{0,^*|0,v*},{^,^*|*,v}}").canonical_form()), "{*,0,{*,^|*,0},{0,^*|*,0}|*,*2,*3,0}")
        self.assertEqual(str(Game("{{*,0|*,v},{*,^|v,v*},{0,^*|0,v*}|{*,v|0},{0,v*|0,v*}}").canonical_form()), "{{*,0|*,v},{*,^|v,v*},{0,^*|0,v*}|0}")
        self.assertEqual(str(Game("{*,0,{*,^|0,v*},{0,^*|*,0},{^,^*|v,v*}|*,{*,*2,0|*,0},{*,^|*,v},{*,^|0,v*}}").canonical_form()), "{0|*,{*,*2,0|*,0}}")
        self.assertEqual(str(Game("{{*,0|v},{0,^*|*,v},{0|v*},{^,^*|0,v*}|0,{*,0|*,*2,0},{*2,0|0,v*}}").canonical_form()), "{*,0|*,0,{*,0|*,*2,0}}")
        self.assertEqual(str(Game("{*,{*,0|*,*2,0},{0,^*|*,v},{0|v*},{^,^*|0,v*}|*,*2,0,{*,^|*,v},{0,^*|0,v*}}").canonical_form()), "{*,0,{*,0|*,*2,0}|*,*2,0}")
        self.assertEqual(str(Game("{*,*2,{*,*2,0|*,v},{*,^|v,v*},{0,^*|0,v*}|{*,0|v},{0,^*|*,0},{0|*,*2},{^,^*|0,v*}}").canonical_form()), "0")
        self.assertEqual(str(Game("{*2,{*,*2,0|*,v},{*,*2,0|0,v*},{^*|0}|0,{*,*2,0|*,0},{*,^|0,v*},{0,^*|0,v*},{^|*,0}}").canonical_form()), "{*2,{*,*2,0|*,v},{*,*2,0|0,v*},{^*|0}|0}")
        self.assertEqual(str(Game("{0,{*,*2,0|0,v*},{*,0|*,*2,0},{*,^|*,v}|{*,0|0,^*},{^,^*|*,*2,0}}").canonical_form()), "{0|{*,0|0,^*},{^,^*|*,*2,0}}")
        self.assertEqual(str(Game("{{*,*2|v},{*,0|*,v},{^|0,v*}|*2,{*,*2|0},{^*|v},{^|*,0}}").canonical_form()), "{{*,*2|v},{*,0|*,v},{^|0,v*}|0}")
        self.assertEqual(str(Game("{{*,0|*,*2,0},{^,^*|0,v*}|{*,*2,0|*,0},{^*|v},{^|*,0}}").canonical_form()), "{{*,0|*,*2,0},{^,^*|0,v*}|0}")
        self.assertEqual(str(Game("{v,{*,*2,0|*,v},{^|0,v*}|*,{*,*2,0|*,v},{*,*2|0},{*,0|0,v*}}").canonical_form()), "{v,{*,*2,0|*,v},{^|0,v*}|0}")
        self.assertEqual(str(Game("{{*,0|0,^*},{0,^*|v,v*}|*,*2,*3,{*,^|*,v},{0,^*|*,v},{0|v*}}").canonical_form()), "0")
        self.assertEqual(str(Game("{*,0,{*,*2,0|0,v*},{*,0|*,*2,0},{0,^*|*,v}|{*,*2,0|*,0},{0|*2}}").canonical_form()), "{0|{*,*2,0|*,0},{0|*2}}")
