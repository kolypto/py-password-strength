from six import with_metaclass

class ATestMeta(type):
    """ Metaclass that collects class names into `ATest.test_classes` dict.

        To define more classes, just subclass `ATest`.
        If class name starts with `_`, it's ignored.
    """

    def __new__(cls, name, bases, attrs):
        is_base = 'test_classes' in attrs
        test_classes = attrs['test_classes'] if is_base else ATest.test_classes

        cls = super(ATestMeta, cls).__new__(cls, name, bases, attrs)
        if not is_base and not name.startswith('_'):
            test_classes[name.lower()] = cls

        return cls


class ATest(with_metaclass(ATestMeta, object)):
    """ ATest is a base class for password tests.

        To create a custom test, just subclass it and implement the following methods:

        * __init__() that takes configuration arguments
        * test(ps) that tests a password, where `ps` is a `PasswordStats` object.
    """
    #: Test classes map: { name : class }
    test_classes = {}

    def __init__(self, *args):
        self.args = args  # Store args

    @classmethod
    def name(cls):
        """ Get test name """
        return cls.__name__.lower()

    def test(self, ps):
        """ Test a password with the test

        :param ps: Password stats
        :type ps: PasswordStats
        :return: Whether the test was passed
        :rtype: bool
        """
        raise NotImplementedError

    def __repr__(self):
        return '{cls}({args})'.format(cls=self.__class__.__name__, args=', '.join(map(str, self.args)))
