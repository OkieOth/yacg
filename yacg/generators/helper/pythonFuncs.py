"""Set of functions to smooth model handling for templates that create
Python code
"""


def getDefaultPythonValue(propertyObj):
    if propertyObj.isArray:
        return '[]'
    else:
        return None
