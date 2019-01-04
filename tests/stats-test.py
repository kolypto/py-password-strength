# -*- coding: utf-8 -*-

import unittest
import six
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
        p2 = '01'
        p8 = '00000001'
        p24 = 'abcdefgh'
        p33 = 'abcdefgh!@'
        p58 = 'abcdefgh!@#$%^&'
        p89 = 'correcthorsebatterystaple'

        p160  = ''.join(six.unichr(n) for n in range(0, 32))
        p384  = ''.join(six.unichr(n) for n in range(0, 64))
        p896  = ''.join(six.unichr(n) for n in range(0, 128))
        p2048 = ''.join(six.unichr(n) for n in range(0, 256))

        self.assertEqual(PasswordStats(p2).combinations,  4)
        self.assertEqual(PasswordStats(p8).combinations,  256)
        self.assertEqual(PasswordStats(p24).combinations, 16777216)

        self.assertAlmostEqual(PasswordStats(   '01').entropy_density,  1.0,  delta=0.01)
        self.assertAlmostEqual(PasswordStats(  '001').entropy_density,  0.63, delta=0.01)
        self.assertAlmostEqual(PasswordStats( '0001').entropy_density,  0.5,  delta=0.01)
        self.assertAlmostEqual(PasswordStats('00001').entropy_density,  0.43, delta=0.01)

        self.assertAlmostEqual(PasswordStats(   p2).entropy_bits, 2.0,     delta=0.01)
        self.assertAlmostEqual(PasswordStats(   p8).entropy_bits, 8.0,     delta=0.01)
        self.assertAlmostEqual(PasswordStats(  p24).entropy_bits, 24.0,    delta=0.01)
        self.assertAlmostEqual(PasswordStats(  p33).entropy_bits, 33.21,   delta=0.01)
        self.assertAlmostEqual(PasswordStats(  p58).entropy_bits, 58.60,   delta=0.01)
        self.assertAlmostEqual(PasswordStats(  p89).entropy_bits, 89.62,   delta=0.01)
        self.assertAlmostEqual(PasswordStats( p160).entropy_bits, 160.00,  delta=0.01)
        self.assertAlmostEqual(PasswordStats( p384).entropy_bits, 384.00,  delta=0.01)
        self.assertAlmostEqual(PasswordStats( p896).entropy_bits, 896.00,  delta=0.01)
        self.assertAlmostEqual(PasswordStats(p2048).entropy_bits, 2048.00, delta=0.01)

        self.assertAlmostEqual(PasswordStats(   p2).strength(), 0.02,   delta=0.01)
        self.assertAlmostEqual(PasswordStats(   p8).strength(), 0.08,   delta=0.01)
        self.assertAlmostEqual(PasswordStats(  p24).strength(), 0.26,   delta=0.01)
        self.assertAlmostEqual(PasswordStats(  p33).strength(), 0.39,   delta=0.01)
        self.assertAlmostEqual(PasswordStats(  p58).strength(), 0.70,   delta=0.01)
        self.assertAlmostEqual(PasswordStats(  p89).strength(), 0.88,   delta=0.01)
        self.assertAlmostEqual(PasswordStats( p160).strength(), 0.98,   delta=0.01)
        self.assertAlmostEqual(PasswordStats( p896).strength(), 0.99,   delta=0.01)
        self.assertAlmostEqual(PasswordStats(p2048).strength(), 1.00,   delta=0.01)

        self.assertAlmostEqual(PasswordStats( p2).weakness_factor, 0.0,   delta=0.01)
        self.assertAlmostEqual(PasswordStats( p8).weakness_factor, 0.875, delta=0.01)
        self.assertAlmostEqual(PasswordStats(p24).weakness_factor, 1.0,   delta=0.01)
        self.assertAlmostEqual(PasswordStats(p89).weakness_factor, 0.16,  delta=0.01)

    def test_detectors(self):
        self.assertEqual(PasswordStats('abcabc-1234').repeated_patterns_length, 6)
        self.assertEqual(PasswordStats('abcabcab-1234').repeated_patterns_length, 6)
        self.assertEqual(PasswordStats('abcabcabc-1234').repeated_patterns_length, 9)

        self.assertEqual(PasswordStats('qazwsx').sequences_length, 0)
        self.assertEqual(PasswordStats('qw...').sequences_length, 0)  # Does not detect 2-character sequences
        self.assertEqual(PasswordStats('qwe...').sequences_length, 3)
        self.assertEqual(PasswordStats('qwerty...').sequences_length, 6)
        self.assertEqual(PasswordStats('ZZqwertyZZ1234...').sequences_length, 10)
