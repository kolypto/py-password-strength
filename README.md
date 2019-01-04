[![Build Status](https://api.travis-ci.org/kolypto/py-password-strength.png?branch=master)](https://travis-ci.org/kolypto/py-password-strength)


Password Strength
=================

Password strength and validation.


PasswordPolicy
==============

Perform tests on a password.

Init Policy
-----------

```python
PasswordPolicy(*tests)
```

Init password policy with a list of tests

Alternatively:

```python
PasswordPolicy.from_names(**tests)
```

Init password policy from a dictionary of test definitions.

A test definition is simply:

    { test-name: argument } or { test-name: [arguments] }

Test name is just a lowercased class name.

Example:

    PasswordPolicy.from_names(
        length=8,
        strength=(0.33, 30),
    )


Bundled Tests
-------------

These objects perform individual tests on a password, and report `True` of `False`.


#### tests.EntropyBits(bits)
Test whether the password has >= `bits` entropy bits

#### tests.Length(length)
Tests whether password length >= `length`

#### tests.NonLetters(count)
Test whether the password has >= `count` non-letter characters

#### tests.NonLettersLc(count)
Test whether the password has >= `count` non-lowercase characters

#### tests.Numbers(count)
Test whether the password has >= `count` numeric characters

#### tests.Special(count)
Test whether the password has >= `count` special characters

#### tests.Strength(strength, weak_bits=30)
Test whether the password has >= `strength` strength.

A password is evaluated to the strength of 0.333 when it has `weak_bits` entropy bits,
which is considered to be a weak password. Strong passwords start at 0.666.

#### tests.Uppercase(count)
Test whether the password has >= `count` uppercase characters


Testing
-------

After the `PasswordPolicy` is initialized, there are two methods to test:

### PasswordPolicy.password
```python
password(password)
```
Get password stats bound to the tests declared in this policy.

If in addition to tests you need to get statistics (e.g. strength) -- use this object to double calculations.

See [`PasswordStats`](#passwordstats) for more details.

### PasswordPolicy.test
```python
test(password)
```
Perform tests on a password.

Shortcut for: `PasswordPolicy.password(password).test()`.


Custom Tests
------------

ATest is a base class for password tests.

To create a custom test, just subclass it and implement the following methods:

* __init__() that takes configuration arguments
* test(ps) that tests a password, where `ps` is a `PasswordStats` object.


PasswordStats
-------------

PasswordStats allows to calculate statistics on a password.

It considers a password as a unicode string, and all statistics are unicode-based.

Constructor:

```python
from password_strength import PasswordStats
PasswordStats(password)
```


#### PasswordStats.alphabet
Get alphabet: set of used characters

#### PasswordStats.alphabet_cardinality
Get alphabet cardinality: alphabet length

#### PasswordStats.char_categories
Character count per top-level category

The following top-level categories are defined:

- L: letter
- M: Mark
- N: Number
- P: Punctuation
- S: Symbol
- Z: Separator
- C: Other

#### PasswordStats.char_categories_detailed
Character count per unicode category, detailed format.

See: http://www.unicode.org/reports/tr44/#GC_Values_Table

#### PasswordStats.combinations
The number of possible combinations with the current alphabet

#### PasswordStats.count(*categories)
Count characters of the specified classes only

#### PasswordStats.count_except(*categories)
Count characters of all classes except the specified ones

#### PasswordStats.entropy_bits
Get information entropy bits: log2 of the number of possible passwords

https://en.wikipedia.org/wiki/Password_strength

#### PasswordStats.entropy_density
Get information entropy density factor, ranged {0 .. 1}.

This is ratio of entropy_bits() to max bits a password of this length could have.
E.g. if all characters are unique -- then it's 1.0.
If half of the characters are reused once -- then it's 0.5.

#### PasswordStats.length
Get password length

#### PasswordStats.letters
Count all letters

#### PasswordStats.letters_lowercase
Count lowercase letters

#### PasswordStats.letters_uppercase
Count uppercase letters

#### PasswordStats.numbers
Count numbers

#### PasswordStats.repeated_patterns_length
Detect and return the length of repeated patterns.

You will probably be comparing it with the length of the password itself and ban if it's longer than 10%

#### PasswordStats.sequences_length
Detect and return the length of used sequences:

- Alphabet letters: abcd...
- Keyboard letters: qwerty, etc
- Keyboard special characters in the top row: ~!@#$%^&*()_+
- Numbers: 0123456

#### PasswordStats.special_characters
Count special characters

Special characters is everything that's not a letter or a number

#### PasswordStats.strength(weak_bits=30)
Get password strength as a number normalized to range {0 .. 1}.

Normalization is done in the following fashion:

1. If entropy_bits <= weak_bits   -- linear in range{0.0 .. 0.33} (weak)
2. If entropy_bits <= weak_bits*2 -- almost linear in range{0.33 .. 0.66} (medium)
3. If entropy_bits > weak_bits*3  -- asymptotic towards 1.0 (strong)

#### PasswordStats.test(tests)
Test the password against a list of tests

#### PasswordStats.weakness_factor
Get weakness factor as a float in range {0 .. 1}

This detects the portion of the string that contains:
* repeated patterns
* sequences

E.g. a value of 1.0 means the whole string is weak, and 0.5 means half of the string is weak.

Typical usage:

password_strength = (1 - weakness_factor) * strength

