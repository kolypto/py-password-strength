import password_strength
from password_strength import PasswordPolicy, PasswordStats
from exdoc import doc, getmembers

import json


def docmodule(module, *predicates):
    return {
        'module': doc(module),
        'attrs': {key: doc(value) for key, value in getmembers(module, *predicates)},
    }


def doccls(cls, *predicates):
    return {
        'class': doc(cls),
        'attrs': {key: doc(value) for key, value in getmembers(cls, *predicates)},
    }


data = {
    'PasswordPolicy': doccls(PasswordPolicy),
    'PasswordStats': doccls(PasswordStats),
    'tests': docmodule(password_strength.tests, lambda key, value: key not in ('ATest',)),
    'ATest': doc(password_strength.tests.ATest),
}

print json.dumps(data, indent=2)
