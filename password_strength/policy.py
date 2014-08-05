from . import PasswordStats
from . import tests as _tests


class PasswordPolicy(object):
    """ Perform tests on a password. """

    @classmethod
    def from_names(cls, **tests):
        """ Init password policy from a dictionary of test definitions.

        A test definition is simply:

            { test-name: argument } or { test-name: [arguments] }

        Example:

            PasswordPolicy.from_names(
                length=8,
                strength=(0.33, 30),
            )

        :param tests: Dict of test definitions.
        :rtype: PasswordPolicy
        :raises KeyError: wrong test name
        """
        tests = [ _tests.ATest.test_classes[name](
                      *(args if isinstance(args, (list, tuple)) else [args])
                  ) for name, args in tests.items() ]
        return PasswordPolicy(*tests)

    def __init__(self, *tests):
        """ Init password policy with tests

        :param ts: List of tests to use for testing passwords
        :type ts: list[tests.ATest]
        """
        self._tests = tests

        assert all(map(lambda c: isinstance(c, _tests.ATest), tests)), 'Tests should be instances of password_strength.tests.ATest'

    def test(self, password):
        """ Perform tests on a password.

        :param password: Passphrase
        :type password: str|unicode|PasswordStats
        :return: list of test objects that have failed
        :rtype: list[tests.ATest]
        """
        ps = password if isinstance(password, PasswordStats) else PasswordStats(password)
        return [t
                for t in self._tests
                if not t.test(ps)]
