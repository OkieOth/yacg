# Attention, this file is generated. Manual changes get lost with the next
# run of the code generation.
# created by yacg (template: pythonBeans.mako v1.0.0)

from enum import Enum


class Job:
    """ base object that describes a complete code generation process
    """

    def __init__(self):

        #: base object that describes a complete code generation process
        self.name = None

        #: base object that describes a complete code generation process
        self.description = None

        #: base object that describes a complete code generation process
        self.models = []

        #: base object that describes a complete code generation process
        self.tasks = []

    @classmethod
    def dictToObject(cls, dict):
        if dict is None:
            return None
        obj = cls()

        obj.name = dict.get('name', None)

        obj.description = dict.get('description', None)

        arrayModels = dict.get('models', [])
        for elemModels in arrayModels:
            obj.models.append(
                Model.dictToObject(elemModels))

        arrayTasks = dict.get('tasks', [])
        for elemTasks in arrayTasks:
            obj.tasks.append(
                Task.dictToObject(elemTasks))
        return obj


class Model:
    """ A model that should be used
    """

    def __init__(self):

        #: A model that should be used
        self.schema = None

        #: A model that should be used
        self.domain = None

        #: A model that should be used
        self.blackListed = []

        #: A model that should be used
        self.whiteListed = []

    @classmethod
    def dictToObject(cls, dict):
        if dict is None:
            return None
        obj = cls()

        obj.schema = dict.get('schema', None)

        obj.domain = dict.get('domain', None)

        arrayBlackListed = dict.get('blackListed', [])
        for elemBlackListed in arrayBlackListed:
            obj.blackListed.append(
                BlackWhiteListEntry.dictToObject(elemBlackListed))

        arrayWhiteListed = dict.get('whiteListed', [])
        for elemWhiteListed in arrayWhiteListed:
            obj.whiteListed.append(
                BlackWhiteListEntry.dictToObject(elemWhiteListed))
        return obj


class Task:
    """ A task to run
    """

    def __init__(self):

        #: A task to run
        self.name = None

        #: A task to run
        self.description = None

        #: A task to run
        self.blackListed = []

        #: A task to run
        self.whiteListed = []

        #: A task to run
        self.singleFileTask = None

        #: A task to run
        self.multiFileTask = None

        #: A task to run
        self.randomDataTask = None

    @classmethod
    def dictToObject(cls, dict):
        if dict is None:
            return None
        obj = cls()

        obj.name = dict.get('name', None)

        obj.description = dict.get('description', None)

        arrayBlackListed = dict.get('blackListed', [])
        for elemBlackListed in arrayBlackListed:
            obj.blackListed.append(
                BlackWhiteListEntry.dictToObject(elemBlackListed))

        arrayWhiteListed = dict.get('whiteListed', [])
        for elemWhiteListed in arrayWhiteListed:
            obj.whiteListed.append(
                BlackWhiteListEntry.dictToObject(elemWhiteListed))

        obj.singleFileTask = SingleFileTask.dictToObject(dict.get('singleFileTask', None))

        obj.multiFileTask = MultiFileTask.dictToObject(dict.get('multiFileTask', None))

        obj.randomDataTask = RandomDataTask.dictToObject(dict.get('randomDataTask', None))
        return obj


class BlackWhiteListEntry:
    """ entry of a type back/white list
    """

    def __init__(self):

        #: entry of a type back/white list
        self.name = None

        #: entry of a type back/white list
        self.type = None

    @classmethod
    def dictToObject(cls, dict):
        if dict is None:
            return None
        obj = cls()

        obj.name = dict.get('name', None)

        obj.type = BlackWhiteListEntryTypeEnum.valueForString(dict.get('type', None))
        return obj


class BlackWhiteListEntryTypeEnum(Enum):
    TYPE = 'type'
    TAG = 'tag'
    CONTAINEDATTRIB = 'containedAttrib'
    NOTCONTAINEDATTRIB = 'notContainedAttrib'
    DOMAIN = 'domain'
    TYPETYPE = 'typeType'

    @classmethod
    def valueForString(cls, stringValue):
        lowerStringValue = stringValue.lower() if stringValue is not None else None
        if lowerStringValue is None:
            return None
        elif lowerStringValue == 'type':
            return BlackWhiteListEntryTypeEnum.TYPE
        elif lowerStringValue == 'tag':
            return BlackWhiteListEntryTypeEnum.TAG
        elif lowerStringValue == 'containedattrib':
            return BlackWhiteListEntryTypeEnum.CONTAINEDATTRIB
        elif lowerStringValue == 'notcontainedattrib':
            return BlackWhiteListEntryTypeEnum.NOTCONTAINEDATTRIB
        elif lowerStringValue == 'domain':
            return BlackWhiteListEntryTypeEnum.DOMAIN
        elif lowerStringValue == 'typetype':
            return BlackWhiteListEntryTypeEnum.TYPETYPE
        else:
            return None

    @classmethod
    def valueAsString(cls, enumValue):
        if enumValue is None:
            return ''
        elif enumValue == BlackWhiteListEntryTypeEnum.TYPE:
            return 'type'
        elif enumValue == BlackWhiteListEntryTypeEnum.TAG:
            return 'tag'
        elif enumValue == BlackWhiteListEntryTypeEnum.CONTAINEDATTRIB:
            return 'containedAttrib'
        elif enumValue == BlackWhiteListEntryTypeEnum.NOTCONTAINEDATTRIB:
            return 'notContainedAttrib'
        elif enumValue == BlackWhiteListEntryTypeEnum.DOMAIN:
            return 'domain'
        elif enumValue == BlackWhiteListEntryTypeEnum.TYPETYPE:
            return 'typeType'
        else:
            return ''



class SingleFileTask:
    """ parameter of a code generation task that creates one file
    """

    def __init__(self):

        #: parameter of a code generation task that creates one file
        self.template = None

        #: parameter of a code generation task that creates one file
        self.destFile = None

        #: parameter of a code generation task that creates one file
        self.templateParams = []

    @classmethod
    def dictToObject(cls, dict):
        if dict is None:
            return None
        obj = cls()

        obj.template = dict.get('template', None)

        obj.destFile = dict.get('destFile', None)

        arrayTemplateParams = dict.get('templateParams', [])
        for elemTemplateParams in arrayTemplateParams:
            obj.templateParams.append(
                TemplateParam.dictToObject(elemTemplateParams))
        return obj


class TemplateParam:
    """ additional, template specific custom parameter for codegen task
    """

    def __init__(self):

        #: additional, template specific custom parameter for codegen task
        self.name = None

        #: additional, template specific custom parameter for codegen task
        self.value = None

        #: additional, template specific custom parameter for codegen task
        self.requiredDomains = []

        #: additional, template specific custom parameter for codegen task
        self.requiredTags = []

        #: additional, template specific custom parameter for codegen task
        self.requiredNames = []

    @classmethod
    def dictToObject(cls, dict):
        if dict is None:
            return None
        obj = cls()

        obj.name = dict.get('name', None)

        obj.value = dict.get('value', None)

        arrayRequiredDomains = dict.get('requiredDomains', [])
        for elemRequiredDomains in arrayRequiredDomains:
            obj.requiredDomains.append(elemRequiredDomains)

        arrayRequiredTags = dict.get('requiredTags', [])
        for elemRequiredTags in arrayRequiredTags:
            obj.requiredTags.append(elemRequiredTags)

        arrayRequiredNames = dict.get('requiredNames', [])
        for elemRequiredNames in arrayRequiredNames:
            obj.requiredNames.append(elemRequiredNames)
        return obj


class MultiFileTask:
    """ parameter of a code generation task that creates one file per model type
    """

    def __init__(self):

        #: parameter of a code generation task that creates one file per model type
        self.template = None

        #: parameter of a code generation task that creates one file per model type
        self.destDir = None

        #: parameter of a code generation task that creates one file per model type
        self.destFilePrefix = None

        #: parameter of a code generation task that creates one file per model type
        self.destFilePostfix = None

        #: parameter of a code generation task that creates one file per model type
        self.destFileExt = None

        #: parameter of a code generation task that creates one file per model type
        self.upperCaseStartedDestFileName = False

        #: parameter of a code generation task that creates one file per model type
        self.fileFilterType = MultiFileTaskFileFilterTypeEnum.TYPE

        #: parameter of a code generation task that creates one file per model type
        self.templateParams = []

        #: parameter of a code generation task that creates one file per model type
        self.createOnlyIfNotExist = False

        #: parameter of a code generation task that creates one file per model type
        self.createTmpFileIfAlreadyExist = False

    @classmethod
    def dictToObject(cls, dict):
        if dict is None:
            return None
        obj = cls()

        obj.template = dict.get('template', None)

        obj.destDir = dict.get('destDir', None)

        obj.destFilePrefix = dict.get('destFilePrefix', None)

        obj.destFilePostfix = dict.get('destFilePostfix', None)

        obj.destFileExt = dict.get('destFileExt', None)

        obj.upperCaseStartedDestFileName = dict.get('upperCaseStartedDestFileName', False)

        obj.fileFilterType = MultiFileTaskFileFilterTypeEnum.valueForString(dict.get('fileFilterType', None))

        arrayTemplateParams = dict.get('templateParams', [])
        for elemTemplateParams in arrayTemplateParams:
            obj.templateParams.append(
                TemplateParam.dictToObject(elemTemplateParams))

        obj.createOnlyIfNotExist = dict.get('createOnlyIfNotExist', False)

        obj.createTmpFileIfAlreadyExist = dict.get('createTmpFileIfAlreadyExist', False)
        return obj


class MultiFileTaskFileFilterTypeEnum(Enum):
    TYPE = 'type'
    OPENAPIOPERATIONID = 'openApiOperationId'

    @classmethod
    def valueForString(cls, stringValue):
        lowerStringValue = stringValue.lower() if stringValue is not None else None
        if lowerStringValue is None:
            return None
        elif lowerStringValue == 'type':
            return MultiFileTaskFileFilterTypeEnum.TYPE
        elif lowerStringValue == 'openapioperationid':
            return MultiFileTaskFileFilterTypeEnum.OPENAPIOPERATIONID
        else:
            return None

    @classmethod
    def valueAsString(cls, enumValue):
        if enumValue is None:
            return ''
        elif enumValue == MultiFileTaskFileFilterTypeEnum.TYPE:
            return 'type'
        elif enumValue == MultiFileTaskFileFilterTypeEnum.OPENAPIOPERATIONID:
            return 'openApiOperationId'
        else:
            return ''



class RandomDataTask:
    def __init__(self):

        self.outputType = None

        self.destDir = None

        self.defaultMinElemCount = 1

        self.defaultMaxElemCount = 10

        self.specialElemCounts = []

        self.defaultKeyPropNames = []

        self.specialKeyPropNames = []

        self.valuePools = []

        self.defaultMinSize = 1

        self.defaultMaxSize = 10

        self.specialArraySizes = []

        self.defaultMaxDepth = 2

        self.specialMaxDepths = []

    @classmethod
    def dictToObject(cls, dict):
        if dict is None:
            return None
        obj = cls()

        obj.outputType = RandomDataTaskOutputTypeEnum.valueForString(dict.get('outputType', None))

        obj.destDir = dict.get('destDir', None)

        obj.defaultMinElemCount = dict.get('defaultMinElemCount', 1)

        obj.defaultMaxElemCount = dict.get('defaultMaxElemCount', 10)

        arraySpecialElemCounts = dict.get('specialElemCounts', [])
        for elemSpecialElemCounts in arraySpecialElemCounts:
            obj.specialElemCounts.append(
                RandomDataTaskSpecialElemCounts.dictToObject(elemSpecialElemCounts))

        arrayDefaultKeyPropNames = dict.get('defaultKeyPropNames', [])
        for elemDefaultKeyPropNames in arrayDefaultKeyPropNames:
            obj.defaultKeyPropNames.append(elemDefaultKeyPropNames)

        arraySpecialKeyPropNames = dict.get('specialKeyPropNames', [])
        for elemSpecialKeyPropNames in arraySpecialKeyPropNames:
            obj.specialKeyPropNames.append(
                RandomDataTaskSpecialKeyPropNames.dictToObject(elemSpecialKeyPropNames))

        arrayValuePools = dict.get('valuePools', [])
        for elemValuePools in arrayValuePools:
            obj.valuePools.append(
                RandomDataTaskValuePools.dictToObject(elemValuePools))

        obj.defaultMinSize = dict.get('defaultMinSize', 1)

        obj.defaultMaxSize = dict.get('defaultMaxSize', 10)

        arraySpecialArraySizes = dict.get('specialArraySizes', [])
        for elemSpecialArraySizes in arraySpecialArraySizes:
            obj.specialArraySizes.append(
                RandomDataTaskSpecialArraySizes.dictToObject(elemSpecialArraySizes))

        obj.defaultMaxDepth = dict.get('defaultMaxDepth', 2)

        arraySpecialMaxDepths = dict.get('specialMaxDepths', [])
        for elemSpecialMaxDepths in arraySpecialMaxDepths:
            obj.specialMaxDepths.append(
                RandomDataTaskSpecialMaxDepths.dictToObject(elemSpecialMaxDepths))
        return obj


class RandomDataTaskOutputTypeEnum(Enum):
    JSON = 'JSON'
    CSV = 'CSV'

    @classmethod
    def valueForString(cls, stringValue):
        lowerStringValue = stringValue.lower() if stringValue is not None else None
        if lowerStringValue is None:
            return None
        elif lowerStringValue == 'json':
            return RandomDataTaskOutputTypeEnum.JSON
        elif lowerStringValue == 'csv':
            return RandomDataTaskOutputTypeEnum.CSV
        else:
            return None

    @classmethod
    def valueAsString(cls, enumValue):
        if enumValue is None:
            return ''
        elif enumValue == RandomDataTaskOutputTypeEnum.JSON:
            return 'JSON'
        elif enumValue == RandomDataTaskOutputTypeEnum.CSV:
            return 'CSV'
        else:
            return ''



class RandomDataTaskSpecialElemCounts:
    def __init__(self):

        self.typeName = None

        self.minElemCount = None

        self.maxElemCount = None

    @classmethod
    def dictToObject(cls, dict):
        if dict is None:
            return None
        obj = cls()

        obj.typeName = dict.get('typeName', None)

        obj.minElemCount = dict.get('minElemCount', None)

        obj.maxElemCount = dict.get('maxElemCount', None)
        return obj


class RandomDataTaskSpecialKeyPropNames:
    def __init__(self):

        self.typeName = None

        self.keyPropName = None

    @classmethod
    def dictToObject(cls, dict):
        if dict is None:
            return None
        obj = cls()

        obj.typeName = dict.get('typeName', None)

        obj.keyPropName = dict.get('keyPropName', None)
        return obj


class RandomDataTaskValuePools:
    def __init__(self):

        self.propertyName = None

        self.useAll = False

        self.values = []

    @classmethod
    def dictToObject(cls, dict):
        if dict is None:
            return None
        obj = cls()

        obj.propertyName = dict.get('propertyName', None)

        obj.useAll = dict.get('useAll', False)

        arrayValues = dict.get('values', [])
        for elemValues in arrayValues:
            obj.values.append(elemValues)
        return obj


class RandomDataTaskSpecialArraySizes:
    def __init__(self):

        self.propertyName = None

        self.minSize = None

        self.maxSize = None

    @classmethod
    def dictToObject(cls, dict):
        if dict is None:
            return None
        obj = cls()

        obj.propertyName = dict.get('propertyName', None)

        obj.minSize = dict.get('minSize', None)

        obj.maxSize = dict.get('maxSize', None)
        return obj


class RandomDataTaskSpecialMaxDepths:
    def __init__(self):

        self.propertyName = None

        self.maxDepth = None

    @classmethod
    def dictToObject(cls, dict):
        if dict is None:
            return None
        obj = cls()

        obj.propertyName = dict.get('propertyName', None)

        obj.maxDepth = dict.get('maxDepth', None)
        return obj


