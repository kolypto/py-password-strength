from .stats import PasswordStats
from . import tests as _tests


class PasswordPolicy(object):
    """ Perform tests on a password. """

    @classmethod
    def all_tests(cls):
        """ Get a dict of available tests

            :returns: { test-name: TestClass }
            :rtype: dict[type]
        """
        return dict(_tests.ATest.test_classes)

    @classmethod
    def from_names(cls, **tests):
        """ Init password policy from a dictionary of test definitions.

        A test definition is simply:

            { test-name: argument } or { test-name: [arguments] }

        Test name is just a lowercased class name.

        Example:

            PasswordPolicy.from_names(
                length=8,
                strength=(0.33, 30),
            )

        :param tests: Dict of test definitions.
        :rtype: PasswordPolicy
        :raises KeyError: wrong test name
        """
        _tests.ATest.test_classes['length'](8)
        tests = [ _tests.ATest.test_classes[name](
                      *(args if isinstance(args, (list, tuple)) else [args])
                  ) for name, args in tests.items() ]
        return cls(*tests)

    def __init__(self, *tests):
        """ Init password policy with a list of tests

        :param ts: List of tests to use for testing passwords
        :type ts: list[tests.ATest]
        """
        self._tests = tests

        assert all([isinstance(c, _tests.ATest) for c in tests]), 'Tests should be instances of password_strength.tests.ATest'

    def password(self, password):
        """ Get password stats bound to the tests declared in this policy.

        If in addition to tests you need to get statistics (e.g. strength) -- use this object to double calculations.

        See [`PasswordStats`](#passwordstats) for more details.

        :param password: Passphrase
        :type password: str|unicode
        :rtype: BoundPasswordStats
        """
        return BoundPasswordStats(password, self)

    def test(self, password):
        """ Perform tests on a password.

        Shortcut for: `PasswordPolicy.password(password).test()`.

        :param password: Passphrase
        :type password: str|unicode
        :return: List of tests that have failed
        :rtype: list[password_strength.tests.ATest]
        """
        return self.password(password).test()


class BoundPasswordStats(PasswordStats):
    """ PasswordStats bound to a PasswordPolicy """

    def __init__(self, password, policy):
        self._policy = policy
        super(BoundPasswordStats, self).__init__(password)

    def test(self):
        return super(BoundPasswordStats, self).test(self._policy._tests)
