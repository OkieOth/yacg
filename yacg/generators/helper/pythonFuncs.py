"""Set of functions to smooth model handling for templates that create
Python code
"""

import yacg.model.model as model


def getDefaultPythonValue(propertyObj):
    if propertyObj.isArray:
        return '[]'
    else:
        if propertyObj.default is not None:
            return getPythonValueForType(propertyObj.type, propertyObj.default)
        else:
            return None


def getPythonValueForType(type, value):
    if (value is None):
        return 'None'
    if (value == 'None'):
        return 'None'
    if (isinstance(type, model.BooleanType)):
        if (value == 'true'):
            return 'True'
        else:
            return 'False'
    elif (isinstance(type, model.StringType)):
        return '''{}'''.format(str(value))
    else:
        return str(value)
