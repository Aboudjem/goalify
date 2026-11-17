"""Tests for the demo project. Run: python3 -m unittest -q test_slugify"""
import unittest

from slugify import slugify


class SlugifyTest(unittest.TestCase):
    def test_lowercases_and_joins_words(self):
        self.assertEqual(slugify("Hello, World!"), "hello-world")

    def test_collapses_spaces_and_symbols(self):
        self.assertEqual(slugify("  A  --  B  "), "a-b")

    def test_keeps_digits(self):
        self.assertEqual(slugify("Release 3.1 notes"), "release-3-1-notes")


if __name__ == "__main__":
    unittest.main()
