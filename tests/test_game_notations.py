import unittest
from cg import game_notations as gn


class TestGameNotations(unittest.TestCase):
    def test_expand_integers(self):
        # Basic integer games
        self.assertEqual(gn.expand_integers("0"), "{|}")
        self.assertEqual(gn.expand_integers("1"), "{{|}|}")
        self.assertEqual(gn.expand_integers("-1"), "{|{|}}")
        self.assertEqual(gn.expand_integers("2"), "{{{|}|}|}")
        self.assertEqual(gn.expand_integers("-2"), "{|{|{|}}}")
        self.assertEqual(gn.expand_integers("{-1|1}"), "{{|{|}}|{{|}|}}")

        # Games without integers
        self.assertEqual(gn.expand_integers("*"), "*")
        self.assertEqual(gn.expand_integers("^"), "^")
        self.assertEqual(gn.expand_integers("v"), "v")
        self.assertEqual(gn.expand_integers("^*"), "^*")
        self.assertEqual(gn.expand_integers("v*"), "v*")
        self.assertEqual(gn.expand_integers("{*|*}"), "{*|*}")

    def test_compress_cgn(self):
        # Basic games
        self.assertEqual(gn.compress_cgn("{|}"), "0")
        self.assertEqual(gn.compress_cgn("{0|}"), "1")
        self.assertEqual(gn.compress_cgn("{|0}"), "-1")
        self.assertEqual(gn.compress_cgn("{0|0}"), "*")
        self.assertEqual(gn.compress_cgn("{*,0|*,0}"), "*2")
        self.assertEqual(gn.compress_cgn("{*,*2,0|*,*2,0}"), "*3")
        self.assertEqual(gn.compress_cgn("{0|*}"), "^")
        self.assertEqual(gn.compress_cgn("{*|0}"), "v")
        self.assertEqual(gn.compress_cgn("{*,0|0}"), "^*")
        self.assertEqual(gn.compress_cgn("{0|*,0}"), "v*")

        # Unsorted options, should not be fixed
        self.assertEqual(gn.compress_cgn("{0,*|0,*}"), "{0,*|0,*}")
        self.assertEqual(gn.compress_cgn("{0,*|*,0}"), "{0,*|*,0}")
        self.assertEqual(gn.compress_cgn("{*,0|0,*}"), "{*,0|0,*}")
        self.assertEqual(gn.compress_cgn("{0,*,*2|0,*,*2}"), "{0,*,*2|0,*,*2}")
        self.assertEqual(gn.compress_cgn("{0,*2,*|*,0,*2}"), "{0,*2,*|*,0,*2}")
        self.assertEqual(gn.compress_cgn("{*2,*,0|*2,0,*}"), "{*2,*,0|*2,0,*}")
        self.assertEqual(gn.compress_cgn("{0|0,*}"), "{0|0,*}")
        self.assertEqual(gn.compress_cgn("{0,*|0}"), "{0,*|0}")

    def test_is_valid_expanded_cgn(self):
        # Valid cgn
        self.assertTrue(gn.is_valid_expanded_cgn("{|}"))
        self.assertTrue(gn.is_valid_expanded_cgn("{{|}|}"))
        self.assertTrue(gn.is_valid_expanded_cgn("{{|},{|}|}"))

        # Invalid cgn
        self.assertFalse(gn.is_valid_expanded_cgn(""))
        self.assertFalse(gn.is_valid_expanded_cgn("|"))
        self.assertFalse(gn.is_valid_expanded_cgn("{"))
        self.assertFalse(gn.is_valid_expanded_cgn("}"))
        self.assertFalse(gn.is_valid_expanded_cgn("{|"))
        self.assertFalse(gn.is_valid_expanded_cgn("|}"))
        self.assertFalse(gn.is_valid_expanded_cgn("||"))
        self.assertFalse(gn.is_valid_expanded_cgn("."))
