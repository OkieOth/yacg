"""Set of functions to smooth model handling for templates that create
Python code
"""

import yacg.model.model as model
import yacg.util.stringUtils as stringUtils


def getDefaultPythonValue(propertyObj):
    if propertyObj.isArray:
        return '[]'
    else:
        if (hasattr(propertyObj.type, 'default')) and (propertyObj.type.default is not None):
            return getPythonValueForType(propertyObj.type, propertyObj.type.default)
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
    elif (isinstance(type, model.EnumType)):
        return '''{}.{}'''.format(type.name, stringUtils.toUpperCaseName(value))
    elif (isinstance(type, model.StringType)):
        return '"{}"'.format(str(value))
    else:
        return str(value)


def getExtendsType(type, modelTypes, baseModelDomain):
    return getTypeWithPackage(type.extendsType, modelTypes, baseModelDomain)


def getTypeWithPackage(type, modelTypes, baseModelDomain):
    for t in modelTypes:
        if (t.name == type.name):
            sameSource = True
            if (hasattr(type, 'source') and (hasattr(t, 'source'))):
                if type.source != t.source:
                    sameSource = False
            if sameSource:
                return type.name

    return getTypeWithPackageEnforced(type, baseModelDomain)


def getTypeWithPackageEnforced(type, baseModelDomain):
    if baseModelDomain is None:
        return type.name
    elif (type.domain is not None) and (type.domain != baseModelDomain):
        return '{}.{}'.format(type.domain, type.name)
    else:
        return type.name
