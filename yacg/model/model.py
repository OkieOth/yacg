'''Model types that are used by yacg. The loaded schemas
will be transalated into this types. These are also the
types that are passed into the templates'''

class Type:
    '''Base class for all types'''
    def __init__(self,name):
        #: name of the type
        self.name = name

        self.isBaseType = True

class IntegerType (Type):
    '''Type to represent Integer and Long types'''

    def __init__(self):
        super().__init__(self.__class__.__name__)
        self.isLong = False


class NumberType (Type):
    '''Type to represent floating point numbers'''

    def __init__(self):
        super().__init__(self.__class__.__name__)


class StringType (Type):
    '''Type to represent texts'''

    def __init__(self):
        super().__init__(self.__class__.__name__)

class UuidType (Type):
    '''Type to represent a uuid'''

    def __init__(self):
        super().__init__(self.__class__.__name__)


class DateType (Type):
    '''Type that represents a date without a time'''

    def __init__(self):
        super().__init__(self.__class__.__name__)


class DateTimeType (Type):
    '''Type that represents a date without a time'''

    def __init__(self):
        super().__init__(self.__class__.__name__)


class EnumType (Type):
    '''Type to represent fixed values sets'''

    def __init__(self, name):
        super().__init__(name)

        #: allowed values for the enum
        self.values = []

        #: scope/domain to that this type belongs
        self.domain = None

        #: from what file the Type was loaded
        self.source = None

        self.isBaseType = False


class ComplexType (Type):
    '''Container type that bundles attributes'''

    def __init__(self, name):
        super().__init__(name)

        #: Additional tags to group types or provide additional context
        self.tags = []

        #: the attributes of that type
        self.properties = []

        #: scope/domain to that this type belongs
        self.domain = None

        #: from what file the Type was loaded
        self.source = None

        #: what is the super class of that type
        self.extendsType = None

        #: references to types that direct inherrited from that type
        self.extendedBy = []

        #: what types hold references of that type
        self.referencedBy = []

        self.isBaseType = False

class Property:
    '''Attribute of a ComplexType'''

    def __init__(self, name, type):
        #: name of the property
        self.name = name

        #: instance of model.Type
        self.type = type

        #: True in case that attribute is an array
        self.isArray = False

        #: Additional tags to group properties or provide additional context
        self.tags = []


class Tag:
    '''Helper class that allows to add keywords to types and
    attributes
    '''

    def __init__(self, name, value = None):
        #: name of the tag
        self.name = name

        #: otional value of a tag
        self.value = value
