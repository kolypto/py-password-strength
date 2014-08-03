# -*- coding: utf-8 -*-

import unittest
from password_strength import PasswordStats


class StatsTest(unittest.TestCase):
    """ Test PasswordStats """

    def test_statistics(self):
        self.assertEqual(PasswordStats('123444').alphabet, set('1234'))
        self.assertEqual(PasswordStats(u'!аб!').alphabet, set(u'!аб'))

        self.assertEqual(PasswordStats('123444').alphabet_cardinality, 4)
        self.assertEqual(PasswordStats(u'!аб!').alphabet_cardinality, 3)

        self.assertEqual(
            dict(PasswordStats(u'aAA111!!!!°°°°°      \0').char_categories_detailed),
            {'Ll': 1, 'Lu': 2, 'Nd': 3, 'Po': 4, 'So': 5, 'Zs': 6, 'Cc': 1}
        )

        self.assertEqual(
            dict(PasswordStats(u'aAA111!!!!°°°°°      \0').char_categories),
            {'L': 3, 'N': 3, 'P': 4, 'S': 5, 'Z': 6, 'C': 1}
        )

    def test_count(self):
        s = PasswordStats(u'aAA111!!!!°°°°°      \0')

        self.assertEqual(s.length, 22)
        self.assertEqual(s.letters, 3)
        self.assertEqual(s.letters_lowercase, 1)
        self.assertEqual(s.letters_uppercase, 2)
        self.assertEqual(s.numbers, 3)
        self.assertEqual(s.count('L', 'N'), 3+3)
        self.assertEqual(s.special_characters, 4+5+6+1)

    def test_security(self):
        self.assertEqual(PasswordStats('1').combinations, 1)
        self.assertEqual(PasswordStats('10').combinations, 4)
        self.assertEqual(PasswordStats('00000001').combinations, 256)
        self.assertEqual(PasswordStats('abcdefgh').combinations, 16777216)

        self.assertEqual(PasswordStats('01').entropy_bits, 2.0)
        self.assertEqual(PasswordStats('00000001').entropy_bits, 8.0)
        self.assertEqual(PasswordStats('abcdefgh').entropy_bits, 24.0)
        self.assertAlmostEqual(PasswordStats('correcthorsebatterystaple').entropy_bits, 89.62, delta=0.01)

    def test_detectors(self):
        self.assertEqual(PasswordStats('abcabc-1234').repeated_patterns_length, 6)
        self.assertEqual(PasswordStats('abcabcab-1234').repeated_patterns_length, 6)
        self.assertEqual(PasswordStats('abcabcabc-1234').repeated_patterns_length, 9)

        self.assertEqual(PasswordStats('qazwsx').sequences_length, 0)
        self.assertEqual(PasswordStats('qwe...').sequences_length, 3)
        self.assertEqual(PasswordStats('qwerty...').sequences_length, 6)
        self.assertEqual(PasswordStats('ZZqwertyZZ1234...').sequences_length, 10)
