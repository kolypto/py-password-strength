`Build Status <https://travis-ci.org/kolypto/py-password-strength>`__
`Pythons <.travis.yml>`__

Password Strength
=================

Password strength and validation.

Tutorial
========

Uppercase, Numbers, Special Characters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You test your passwords using the Policy object that controls what kind
of password is acceptable in your system.

First, create the Policy object and define the rules that apply to
passwords in your system:

.. code:: python

   from password_strength import PasswordPolicy

   policy = PasswordPolicy.from_names(
       length=8,  # min length: 8
       uppercase=2,  # need min. 2 uppercase letters
       numbers=2,  # need min. 2 digits
       special=2,  # need min. 2 special characters
       nonletters=2,  # need min. 2 non-letter characters (digits, specials, anything)
   )

Now, when you have the ``PasswordPolicy`` object, you can use it to test
your passwords, and it will tell you which tests have failed:

.. code:: python

   policy.test('ABcd12!')
   # -> [Length(8), Special(2)]

This tells us that 2 tests have failed: password is not long enough, and
it does not have enough special characters. You can use this information
to tell the user what precisely is wrong with their password.

.. code:: python

   policy.test('ABcd12!@')
   # -> []

Empty list tells us that this password is alright.

This test, however, enabled uses to use passwords that have a lot of
repetition.

So-Called Entropy Bits
~~~~~~~~~~~~~~~~~~~~~~

Here’s a test that’s even better. You don’t really need to define
complex rules with special characters and stuff. All you actually need
is a password that’s long enough, complex enough, and easy to remember
(see `xkcd <https://xkcd.com/936/>`__ and `Article: Everything We’ve
Been Told About Passwords Is
Wrong <https://www.inc.com/thomas-koulopoulos/all-that-advice-about-passwords-turns-out-to-be-to.html>`__).

So, instead of defining all these rules, let’s just require the password
to be complex enough. Entropy bits is something that defines how much
variety does your password have. ‘01111010010011’ is long enough, but
has only 2 entropy bits: that’s how many bits you need to store its
alphabet. However, a password that uses plenty of characters has more
entropy.

.. code:: python

   policy = PasswordPolicy.from_names(
       entropybits=30  # need a password that has minimum 30 entropy bits (the power of its alphabet)
   )

   print(policy.test('0123456789'))
   # -> []

This password is not long enough, or secure enough, but has enough
entropy: its vocabulary has 10 different characters. Put this test
together with other requirements to make sure there’s no repetition in
your passwords.

Complexity
~~~~~~~~~~

Entropy bits are important, but difficult to understand. An even better,
more intuitive test, is to require the password to be “complex enough”.
Complexity is a number in the range of 0.00..0.99. Good, strong
passwords start at 0.66.

Let’s first see how different passwords score:

.. code:: python

   from password_strength import PasswordStats

   stats = PasswordStats('qwerty123')
   print(stats.strength())  #-> Its strength is 0.316

   stats = PasswordStats('G00dPassw0rd?!')
   print(stats.strength())  #-> Its strength is 0.585

   stats = PasswordStats('V3ryG00dPassw0rd?!')
   print(stats.strength())  #-> Its strength is 0.767

So, 0.66 will be a very good indication of a good password. Let’s
implement our policy:

.. code:: python

   policy = PasswordPolicy.from_names(
       strength=0.66  # need a password that scores at least 0.5 with its strength
   )

   print(policy.test('V3ryG00dPassw0rd?!'))
   # -> []  -- empty list means a good password

One good thing about using strength is that it allows users to use
national aplhabets with passwords, which are most secure:

.. code:: python

   tested_pass = policy.password('Mixed-汉堡包/漢堡包, 汉堡/漢堡')
   print(tested_pass.strength())  # -> 0.812 -- very good!
   print(tested_pass.test())
   #-> []  - good password; it actually scored 0.812

Notice how in the last example we use a different approach:
``policy.password()`` analyzes the password, and then we can both get
its ``.strength()``, and ``.test()`` it according to the current policy.

PasswordPolicy
==============

Perform tests on a password.

Init Policy
-----------

.. code:: python

   PasswordPolicy(*tests)

Init password policy with a list of tests

Alternatively:

.. code:: python

   PasswordPolicy.from_names(**tests)

Init password policy from a dictionary of test definitions.

A test definition is simply:

::

   { test-name: argument } or { test-name: [arguments] }

Test name is just a lowercased class name.

Example:

::

   PasswordPolicy.from_names(
       length=8,
       strength=(0.33, 30),
   )

Bundled Tests
-------------

These objects perform individual tests on a password, and report
``True`` of ``False``.

tests.EntropyBits(bits)
^^^^^^^^^^^^^^^^^^^^^^^

Test whether the password has >= ``bits`` entropy bits.

Entropy bits is the number of bits that is required to store the
alphabet that’s used in a password. It’s a measure of how long is the
alphabet.

tests.Length(length)
^^^^^^^^^^^^^^^^^^^^

Tests whether password length >= ``length``

tests.NonLetters(count)
^^^^^^^^^^^^^^^^^^^^^^^

Test whether the password has >= ``count`` non-letter characters

tests.NonLettersLc(count)
^^^^^^^^^^^^^^^^^^^^^^^^^

Test whether the password has >= ``count`` non-lowercase characters

tests.Numbers(count)
^^^^^^^^^^^^^^^^^^^^

Test whether the password has >= ``count`` numeric characters

tests.Special(count)
^^^^^^^^^^^^^^^^^^^^

Test whether the password has >= ``count`` special characters

tests.Strength(strength, weak_bits=30)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Test whether the password has >= ``strength`` strength.

A password is evaluated to the strength of 0.333 when it has
``weak_bits`` entropy bits, which is considered to be a weak password.
Strong passwords start at 0.666.

tests.Uppercase(count)
^^^^^^^^^^^^^^^^^^^^^^

Test whether the password has >= ``count`` uppercase characters

Testing
-------

After the ``PasswordPolicy`` is initialized, there are two methods to
test:

PasswordPolicy.password
~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

   password(password)

Get password stats bound to the tests declared in this policy.

If in addition to tests you need to get statistics (e.g. strength) – use
this object to double calculations.

See ```PasswordStats`` <#passwordstats>`__ for more details.

PasswordPolicy.test
~~~~~~~~~~~~~~~~~~~

.. code:: python

   test(password)

Perform tests on a password.

Shortcut for: ``PasswordPolicy.password(password).test()``.

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

PasswordStats.alphabet
^^^^^^^^^^^^^^^^^^^^^^

Get alphabet: set of used characters

PasswordStats.alphabet_cardinality
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Get alphabet cardinality: alphabet length

PasswordStats.char_categories
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Character count per top-level category

The following top-level categories are defined:

-  L: letter
-  M: Mark
-  N: Number
-  P: Punctuation
-  S: Symbol
-  Z: Separator
-  C: Other

PasswordStats.char_categories_detailed
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Character count per unicode category, detailed format.

See: http://www.unicode.org/reports/tr44/#GC_Values_Table

PasswordStats.combinations
^^^^^^^^^^^^^^^^^^^^^^^^^^

The number of possible combinations with the current alphabet

PasswordStats.count(*categories) Count characters of the specified classes only
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

PasswordStats.count_except(*categories) Count characters of all classes except the specified ones
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

PasswordStats.entropy_bits
^^^^^^^^^^^^^^^^^^^^^^^^^^

Get information entropy bits: log2 of the number of possible passwords

https://en.wikipedia.org/wiki/Password_strength

PasswordStats.entropy_density
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Get information entropy density factor, ranged {0 .. 1}.

This is ratio of entropy_bits() to max bits a password of this length
could have. E.g. if all characters are unique – then it’s 1.0. If half
of the characters are reused once – then it’s 0.5.

PasswordStats.length
^^^^^^^^^^^^^^^^^^^^

Get password length

PasswordStats.letters
^^^^^^^^^^^^^^^^^^^^^

Count all letters

PasswordStats.letters_lowercase
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Count lowercase letters

PasswordStats.letters_uppercase
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Count uppercase letters

PasswordStats.numbers
^^^^^^^^^^^^^^^^^^^^^

Count numbers

PasswordStats.repeated_patterns_length
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Detect and return the length of repeated patterns.

You will probably be comparing it with the length of the password itself
and ban if it’s longer than 10%

PasswordStats.sequences_length
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Detect and return the length of used sequences:

-  Alphabet letters: abcd…
-  Keyboard letters: qwerty, etc
-  Keyboard special characters in the top row: ~!@#$%^&*()_+
-  Numbers: 0123456

PasswordStats.special_characters
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Count special characters

Special characters is everything that’s not a letter or a number

PasswordStats.strength(weak_bits=30)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Get password strength as a number normalized to range {0 .. 1}.

Normalization is done in the following fashion:

1. If entropy_bits <= weak_bits – linear in range{0.0 .. 0.33} (weak)
2. If entropy_bits <= weak_bits*2 – almost linear in range{0.33 .. 0.66}
   (medium)
3. If entropy_bits > weak_bits*3 – asymptotic towards 1.0 (strong)

PasswordStats.test(tests)
^^^^^^^^^^^^^^^^^^^^^^^^^

Test the password against a list of tests

PasswordStats.weakness_factor
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Get weakness factor as a float in range {0 .. 1}

This detects the portion of the string that contains: \* repeated
patterns \* sequences

E.g. a value of 1.0 means the whole string is weak, and 0.5 means half
of the string is weak.

Typical usage:

password_strength = (1 - weakness_factor) \* strength
