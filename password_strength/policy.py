from . import PasswordStats
from . import tests as _tests


class PasswordPolicy(object):
    """ Password policy tester """

    def __init__(self, *tests):
        """ Init password policy with tests

        :param ts: List of tests to use for testing passwords
        :type ts: list[tests.BaseTest]
        """
        self._tests = tests

        assert all(map(lambda c: isinstance(c, _tests.BaseTest), tests)), 'Tests should be instances of password_strength.tests.BaseTest'

    def test(self, password):
        """ Test a password

        :param password: Passphrase
        :type password: str|unicode|PasswordStats
        :return: List of test objects that have failed
        :rtype: list[tests.BaseTest]
        """
        ps = password if isinstance(password, PasswordStats) else PasswordStats(password)
        return [t
                for t in self._tests
                if not t.test(ps)]
