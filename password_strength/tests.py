from tests_base import ATest


class Length(ATest):
    """ Password length >= the required minimum length """

    def __init__(self, length):
        self.length = length

    def test(self, ps):
        return ps.length >= self.length


class Uppercase(ATest):
    """ Has enough uppercase characters """

    def __init__(self, count):
        self.count = count

    def test(self, ps):
        return ps.letters_uppercase >= self.count


class Numbers(Uppercase):
    """ Has enough numbers """

    def test(self, ps):
        return ps.numbers >= self.count


class Special(Uppercase):
    """ Has enough special characters """

    def test(self, ps):
        return ps.special_characters >= self.count


class NonLetters(Uppercase):
    """ Has enough non-letter characters """

    def test(self, ps):
        non_letters = ps.length - ps.letters
        return non_letters >= self.count


class NonLettersLc(Uppercase):
    """ Has enough non-lowercase-letter characters """

    def test(self, ps):
        non_lowercase_letters = ps.length - ps.letters_lowercase
        return non_lowercase_letters >= self.count


class EntropyBits(ATest):
    """ Has enough entropy bits """

    def __init__(self, bits):
        self.bits = bits

    def test(self, ps):
        return ps.entropy_bits >= self.bits


class Strength(ATest):
    """ Has enough strength """

    def __init__(self, strength, weak_bits=30):
        self.strength = strength
        self.weak_bits = weak_bits

    def test(self, ps):
        return (1 - ps.weakness_factor) * ps.strength(self.weak_bits) >= self.strength
