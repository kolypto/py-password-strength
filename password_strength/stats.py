from __future__ import division

import unicodedata
from collections import Counter
from math import log
import re
from functools import wraps
import sys, six

try:  # Python 2
    from itertools import izip as zip
except ImportError:
    pass  # Python 3


def cached_property(f):
    """ Property that will replace itself with a calculated value """
    name = '__' + f.__name__

    @wraps(f)
    def wrapper(self):
        if not hasattr(self, name):
            setattr(self, name, f(self))
        return getattr(self, name)
    return property(wrapper)


class PasswordStats(object):
    """ PasswordStats allows to calculate statistics on a password.

        It considers a password as a unicode string, and all statistics are unicode-based.
    """

    def __init__(self, password):
        self.password = six.text_type(password)

    #region Statistics

    @cached_property
    def alphabet(self):
        """ Get alphabet: set of used characters

        :rtype: set
        """
        return set(self.password)

    @cached_property
    def alphabet_cardinality(self):
        """ Get alphabet cardinality: alphabet length

        :rtype: int
        """
        return len(self.alphabet)

    @cached_property
    def char_categories_detailed(self):
        """ Character count per unicode category, detailed format.

        See: http://www.unicode.org/reports/tr44/#GC_Values_Table

        :returns: Counter( unicode-character-category: count )
        :rtype: collections.Counter
        """
        return Counter(map(unicodedata.category, self.password))

    @cached_property
    def char_categories(self):
        """ Character count per top-level category

        The following top-level categories are defined:

        - L: letter
        - M: Mark
        - N: Number
        - P: Punctuation
        - S: Symbol
        - Z: Separator
        - C: Other

        :return: Counter(unicode-character-category: count }
        :rtype: collections.Counter
        """
        c = Counter()
        for cat, n in self.char_categories_detailed.items():
            c[cat[0]] += n
        return c

    #endregion

    #region Counters

    @cached_property
    def length(self):
        """ Get password length

        :rtype: int
        """
        return len(self.password)

    @cached_property
    def letters(self):
        """ Count all letters

        :rtype: int
        """
        return self.char_categories['L']

    @cached_property
    def letters_uppercase(self):
        """ Count uppercase letters

        :rtype: int
        """
        return self.char_categories_detailed['Lu']

    @cached_property
    def letters_lowercase(self):
        """ Count lowercase letters

        :rtype: int
        """
        return self.char_categories_detailed['Ll']

    @cached_property
    def numbers(self):
        """ Count numbers

        :rtype: int
        """
        return self.char_categories['N']

    def count(self, *categories):
        """ Count characters of the specified classes only

        :param categories: Character categories to count
        :type categories: Iterable
        :rtype: int
        """
        return sum([int(cat_n[0] in categories) * cat_n[1] for cat_n in list(self.char_categories.items())])

    def count_except(self, *categories):
        """ Count characters of all classes except the specified ones

        :param categories: Character categories to exclude from count
        :type categories: Iterable
        :rtype: int
        """
        return sum([int(cat_n1[0] not in categories) * cat_n1[1] for cat_n1 in list(self.char_categories.items())])

    @cached_property
    def special_characters(self):
        """ Count special characters

        Special characters is everything that's not a letter or a number

        :rtype: int
        """
        return self.count_except('L', 'N')

    #region Security

    @cached_property
    def combinations(self):
        """ The number of possible combinations with the current alphabet

        :rtype: long
        """
        return self.alphabet_cardinality ** self.length

    @cached_property
    def entropy_bits(self):
        """ Get information entropy bits: log2 of the number of possible passwords

        https://en.wikipedia.org/wiki/Password_strength

        :rtype: float
        """
        return self.length * log(self.alphabet_cardinality, 2)

    @cached_property
    def entropy_density(self):
        """ Get information entropy density factor, ranged {0 .. 1}.

        This is ratio of entropy_bits() to max bits a password of this length could have.
        E.g. if all characters are unique -- then it's 1.0.
        If half of the characters are reused once -- then it's 0.5.

        :rtype: float
        """
        # Simplifying:
        #     entropy_bits / (length * log(length, 2)) =
        #   = log(alphabet_cardinality, 2) / log(length, 2) =
        #   = log(alphabet_cardinality, length)
        return log(self.alphabet_cardinality, self.length)

    def strength(self, weak_bits=30):
        """ Get password strength as a number normalized to range {0 .. 1}.

        Normalization is done in the following fashion:

        1. If entropy_bits <= weak_bits   -- linear in range{0.0 .. 0.33} (weak)
        2. If entropy_bits <= weak_bits*2 -- almost linear in range{0.33 .. 0.66} (medium)
        3. If entropy_bits > weak_bits*3  -- asymptotic towards 1.0 (strong)

        :param weak_bits: Minimum entropy bits a medium password should have.
        :type weak_bits: int
        :return: Normalized password strength:
            * <0.33 is WEAK
            * <0.66 is MEDIUM
            * >0.66 is STRONG
        :rtype: float
        """
        WEAK_MAX = 0.333333333

        if self.entropy_bits <= weak_bits:
            return WEAK_MAX * self.entropy_bits / weak_bits

        HARD_BITS = weak_bits*3
        HARD_VAL = 0.950

        # Here, we want a function that:
        # 1. f(x)=0.333 at x=weak_bits
        # 2. f(x)=0.950 at x=weak_bits*3 (great estimation for a perfect password)
        # 3. f(x) is almost linear in range{weak_bits .. weak_bits*2}: doubling the bits should double the strength
        # 4. f(x) has an asymptote of 1.0 (normalization)

        # First, the function:
        #       f(x) = 1 - (1-WEAK_MAX)*2^( -k*x)

        # Now, the equation:
        #       f(HARD_BITS) = HARD_VAL
        #       1 - (1-WEAK_MAX)*2^( -k*HARD_BITS) = HARD_VAL
        #                        2^( -k*HARD_BITS) = (1 - HARD_VAL) / (1-WEAK_MAX)
        #       k = -log2((1 - HARD_VAL) / (1-WEAK_MAX)) / HARD_BITS
        k = -log((1 - HARD_VAL) / (1-WEAK_MAX), 2) / HARD_BITS
        f = lambda x: 1 - (1-WEAK_MAX)*pow(2, -k*x)

        return f(self.entropy_bits - weak_bits)  # with offset

    #endregion

    #region Detectors

    _repeated_patterns_rex = re.compile(r'((.+?)\2+)', re.UNICODE | re.DOTALL | re.IGNORECASE)

    @cached_property
    def repeated_patterns_length(self):
        """ Detect and return the length of repeated patterns.

        You will probably be comparing it with the length of the password itself and ban if it's longer than 10%

        :rtype: int
        """
        length = 0
        for substring, pattern in self._repeated_patterns_rex.findall(self.password):
            length += len(substring)
        return length

    _sequences = (
        'abcdefghijklmnopqrstuvwxyz'  # Alphabet
        'qwertyuiopasdfghjklzxcvbnm'  # Keyboard
        '~!@#$%^&*()_+-='  # Keyboard special, top row
        '01234567890'  # Numbers
    )
    _sequences = _sequences + _sequences[::-1]  # reversed

    @cached_property
    def sequences_length(self):
        """ Detect and return the length of used sequences:

        - Alphabet letters: abcd...
        - Keyboard letters: qwerty, etc
        - Keyboard special characters in the top row: ~!@#$%^&*()_+
        - Numbers: 0123456

        :return: Total length of character sequences that are subsets of the common sequences
        :rtype: int
        """
        # FIXME: Optimize this. I'm sure there is a better way!...
        sequences_length = 0

        # Iterate through the string, with manual variable (to allow skips)
        i = 0
        while i < len(self.password):
            # Slice (since we use it often)
            password = self.password[i:]

            # Iterate over sequences to find longest common prefix
            j = -1
            common_length = 1
            while True:
                # Detect the first match with the current character
                # A character may appear multiple times
                j = self._sequences.find(password[0], j+1)
                if j == -1:
                    break

                # Find the longest common prefix
                common_here = ''
                for a, b in zip(password, self._sequences[j:]):
                    if a != b: break
                    else: common_here += a

                # It it's longer than previous discoveries -- store it
                common_length = max(common_length, len(common_here))

            # Repeated sequence?
            if common_length > 2:
                sequences_length += common_length

            # Next: skip to the end of the detected sequence
            i += common_length

        return sequences_length

    @cached_property
    def weakness_factor(self):
        """ Get weakness factor as a float in range {0 .. 1}

        This detects the portion of the string that contains:
        * repeated patterns
        * sequences

        E.g. a value of 1.0 means the whole string is weak, and 0.5 means half of the string is weak.

        Typical usage:

        password_strength = (1 - weakness_factor) * strength

        :return: Weakness factor
        :rtype: float
        """
        return min(1.0, (self.repeated_patterns_length + self.sequences_length) / self.length)

    #endregion

    def test(self, tests):
        """ Test the password against a list of tests

        :param tests: Test to do
        :type tests: Iterable[password_strength.tests.ATest]
        :return: list of tests that have failed
        :rtype: list[tests.ATest]
        """
        return [t
                for t in tests
                if not t.test(self)]
