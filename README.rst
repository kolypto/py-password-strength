|Build Status|

Password Strength
=================

Password strength and validation.

PasswordPolicy
==============

Perform tests on a password.

Bundled Tests
-------------

These objects perform individual tests on a password, and report
``True`` of ``False``.

tests.Strength(strength, weak\_bits=30)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Test whether the password has >= ``strength`` strength.

A password is evaluated to the strength of 0.333 when it has
``weak_bits`` entropy bits, which is considered to be a weak password.
Strong passwords start at 0.666.

tests.Special(count)
~~~~~~~~~~~~~~~~~~~~

Test whether the password has >= ``count`` special characters

tests.Uppercase(count)
~~~~~~~~~~~~~~~~~~~~~~

Test whether the password has >= ``count`` uppercase characters

tests.EntropyBits(bits)
~~~~~~~~~~~~~~~~~~~~~~~

Test whether the password has >= ``bits`` entropy bits

tests.Length(length)
~~~~~~~~~~~~~~~~~~~~

Tests whether password length >= ``length``

tests.Numbers(count)
~~~~~~~~~~~~~~~~~~~~

Test whether the password has >= ``count`` numeric characters

tests.NonLetters(count)
~~~~~~~~~~~~~~~~~~~~~~~

Test whether the password has >= ``count`` non-letter characters

tests.NonLettersLc(count)
~~~~~~~~~~~~~~~~~~~~~~~~~

Test whether the password has >= ``count`` non-lowercase characters

Usage
-----

First, initialize a ``PasswordPolicy`` object with a list of initialized
tests:

::

    PasswordPolicy(*tests)

Alternatively, you can use ``from_names(**tests)``, which uses a
dictionary. Init password policy from a dictionary of test definitions.

A test definition is simply:

::

    { test-name: argument } or { test-name: [arguments] }

Example:

::

    PasswordPolicy.from_names(
        length=8,
        strength=(0.33, 30),
    )

Having an object, perform tests on a password with:

::

    test(password)

Given a password, it returns list of test objects that have failed

Custom Tests
------------

ATest is a base class for password tests.

To create a custom test, just subclass it and implement the following
methods:

-  **init**\ () that takes configuration arguments
-  test(ps) that tests a password, where ``ps`` is a ``PasswordStats``
   object.

PasswordStats
-------------

PasswordStats allows to calculate statistics on a password.

It considers a password as a unicode string, and all statistics are
unicode-based.

Constructor:

.. code:: python

    from password_strength import PasswordStats
    PasswordStats(password)

PasswordStats.alphabet\_cardinality
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Get alphabet cardinality: alphabet length

PasswordStats.count(\*categories) Count characters of the specified classes only
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PasswordStats.entropy\_bits
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Get information entropy bits: log2 of the number of possible passwords

https://en.wikipedia.org/wiki/Password\_strength

PasswordStats.strength(weak\_bits=30)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Get password strength as a number normalized to range {0 .. 1}.

Normalization is done in the following fashion:

1. If entropy\_bits <= weak\_bits -- linear in range{0.0 .. 0.33} (weak)
2. If entropy\_bits <= weak\_bits\*2 -- almost linear in range{0.33 ..
   0.66} (medium)
3. If entropy\_bits > weak\_bits\*3 -- asymptotic towards 1.0 (strong)

PasswordStats.letters
~~~~~~~~~~~~~~~~~~~~~

Count all letters

PasswordStats.sequences\_length
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Detect and return the length of used sequences:

-  Alphabet letters: abcd...
-  Keyboard letters: qwerty, etc
-  Keyboard special characters in the top row: ~!@#$%^&\*()\_+
-  Numbers: 0123456

PasswordStats.letters\_uppercase
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Count uppercase letters

PasswordStats.alphabet
~~~~~~~~~~~~~~~~~~~~~~

Get alphabet: set of used characters

PasswordStats.weakness\_factor
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Get weakness factor as a float in range {0 .. 1}

This detects the portion of the string that contains: \* repeated
patterns \* sequences

E.g. a value of 1.0 means the whole string is weak, and 0.5 means half
of the string is weak.

Typical usage:

password\_strength = (1 - weakness\_factor) \* strength

PasswordStats.char\_categories
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Character count per top-level category

The following top-level categories are defined:

-  L: letter
-  M: Mark
-  N: Number
-  P: Punctuation
-  S: Symbol
-  Z: Separator
-  C: Other

PasswordStats.length
~~~~~~~~~~~~~~~~~~~~

Get password length

PasswordStats.repeated\_patterns\_length
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Detect and return the length of repeated patterns.

You will probably be comparing it with the length of the password itself
and ban if it's longer than 10%

PasswordStats.letters\_lowercase
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Count lowercase letters

PasswordStats.special\_characters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Count special characters

Special characters is everything that's not a letter or a number

PasswordStats.numbers
~~~~~~~~~~~~~~~~~~~~~

Count numbers

PasswordStats.count\_except(\*categories) Count characters of all classes except the specified ones
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PasswordStats.combinations
~~~~~~~~~~~~~~~~~~~~~~~~~~

The number of possible combinations with the current alphabet

PasswordStats.entropy\_density
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Get information entropy density factor, ranged {0 .. 1}.

This is ratio of entropy\_bits() to max bits a password of this length
could have. E.g. if all characters are unique -- then it's 1.0. If half
of the characters are reused once -- then it's 0.5.

PasswordStats.char\_categories\_detailed
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Character count per unicode category, detailed format.

See: http://www.unicode.org/reports/tr44/#GC\_Values\_Table

.. |Build Status| image:: https://api.travis-ci.org/kolypto/py-password-strength.png?branch=master
   :target: https://travis-ci.org/kolypto/py-password-strength
