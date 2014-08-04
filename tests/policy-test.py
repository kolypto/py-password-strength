import unittest
from password_strength import PasswordPolicy, tests


class PolicyTest(unittest.TestCase):
    """ Test: PasswordPolicy """
    longMessage = True

    def test(self):
        policy = PasswordPolicy(
            tests.Length(8),
            tests.Uppercase(2),
            tests.Numbers(2),
            tests.Special(2),
            tests.NonLetters(2),
            tests.NonLettersLc(2),
            tests.EntropyBits(30),
            tests.Strength(0.3333),
        )

        passwords = {
            'qazwsx':           {'length', 'uppercase', 'numbers', 'special', 'nonletters', 'nonletterslc', 'entropybits', 'strength'},
            'qazwsxrfv':        {          'uppercase', 'numbers', 'special', 'nonletters', 'nonletterslc', 'entropybits', 'strength'},
            'qazwsxrfvTG':      {                       'numbers', 'special', 'nonletters',                                          },
            'qazwsxrfvTG94':    {                                  'special',                                                        },
            'qazwsxrfvTG94@$':  set(),
        }

        for password, expects in passwords.items():
            self.assertEqual(
                {t.name() for t in policy.test(password)},
                expects,
                'Testing {}'.format(password)
            )
