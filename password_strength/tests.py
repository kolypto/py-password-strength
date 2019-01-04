""" These objects perform individual tests on a password, and report `True` of `False`. """

from .tests_base import ATest


class Length(ATest):
    """ Tests whether password length >= `length` """

    def __init__(self, length):
        super(Length, self).__init__(length)
        self.length = length

    def test(self, ps):
        return ps.length >= self.length


class Uppercase(ATest):
    """ Test whether the password has >= `count` uppercase characters """

    def __init__(self, count):
        super(Uppercase, self).__init__(count)
        self.count = count

    def test(self, ps):
        return ps.letters_uppercase >= self.count


class Numbers(Uppercase):
    """ Test whether the password has >= `count` numeric characters """

    def test(self, ps):
        return ps.numbers >= self.count


class Special(Uppercase):
    """ Test whether the password has >= `count` special characters """

    def test(self, ps):
        return ps.special_characters >= self.count


class NonLetters(Uppercase):
    """ Test whether the password has >= `count` non-letter characters """

    def test(self, ps):
        non_letters = ps.length - ps.letters
        return non_letters >= self.count


class NonLettersLc(Uppercase):
    """ Test whether the password has >= `count` non-lowercase characters """

    def test(self, ps):
        non_lowercase_letters = ps.length - ps.letters_lowercase
        return non_lowercase_letters >= self.count


class EntropyBits(ATest):
    """ Test whether the password has >= `bits` entropy bits.

    Entropy bits is the number of bits that is required to store the alphabet that's used in a password.
    It's a measure of how long is the alphabet.

    """

    def __init__(self, bits):
        super(EntropyBits, self).__init__(bits)
        self.bits = bits

    def test(self, ps):
        return ps.entropy_bits >= self.bits


class Strength(ATest):
    """ Test whether the password has >= `strength` strength.

        A password is evaluated to the strength of 0.333 when it has `weak_bits` entropy bits,
        which is considered to be a weak password. Strong passwords start at 0.666.
    """

    def __init__(self, strength, weak_bits=30):
        super(Strength, self).__init__(strength, weak_bits)
        self.strength = strength
        self.weak_bits = weak_bits

    def test(self, ps):
        return (1 - ps.weakness_factor) * ps.strength(self.weak_bits) >= self.strength
