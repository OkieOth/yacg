# Attention, this file is generated. Manual changes get lost with the next
# run of the code generation.
# created by yacg (template: pythonBeans.mako v1.0.0)

from enum import Enum


class Job:
    """ base object that describes a complete code generation process
    """

    def __init__(self, dictObj = None):

        #: base object that describes a complete code generation process
        self.name = None

        #: base object that describes a complete code generation process
        self.description = None

        #: base object that describes a complete code generation process
        self.models = []

        #: base object that describes a complete code generation process
        self.tasks = []
        if dictObj is not None:
            self.initFromDict(dictObj)

    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        self.name = dictObj.get('name', None)

        self.description = dictObj.get('description', None)

        arrayModels = dictObj.get('models', [])
        for elemModels in arrayModels:
            self.models.append(
                Model(elemModels))

        arrayTasks = dictObj.get('tasks', [])
        for elemTasks in arrayTasks:
            self.tasks.append(
                Task(elemTasks))


class Model:
    """ A model that should be used
    """

    def __init__(self, dictObj = None):

        #: A model that should be used
        self.schema = None

        #: A model that should be used
        self.domain = None

        #: A model that should be used
        self.blackListed = []

        #: A model that should be used
        self.whiteListed = []
        if dictObj is not None:
            self.initFromDict(dictObj)

    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        self.schema = dictObj.get('schema', None)

        self.domain = dictObj.get('domain', None)

        arrayBlackListed = dictObj.get('blackListed', [])
        for elemBlackListed in arrayBlackListed:
            self.blackListed.append(
                BlackWhiteListEntry(elemBlackListed))

        arrayWhiteListed = dictObj.get('whiteListed', [])
        for elemWhiteListed in arrayWhiteListed:
            self.whiteListed.append(
                BlackWhiteListEntry(elemWhiteListed))


class Task:
    """ A task to run
    """

    def __init__(self, dictObj = None):

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
        if dictObj is not None:
            self.initFromDict(dictObj)

    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        self.name = dictObj.get('name', None)

        self.description = dictObj.get('description', None)

        arrayBlackListed = dictObj.get('blackListed', [])
        for elemBlackListed in arrayBlackListed:
            self.blackListed.append(
                BlackWhiteListEntry(elemBlackListed))

        arrayWhiteListed = dictObj.get('whiteListed', [])
        for elemWhiteListed in arrayWhiteListed:
            self.whiteListed.append(
                BlackWhiteListEntry(elemWhiteListed))

        self.singleFileTask = SingleFileTask(dict.get('singleFileTask', None))

        self.multiFileTask = MultiFileTask(dict.get('multiFileTask', None))

        self.randomDataTask = RandomDataTask(dict.get('randomDataTask', None))


class BlackWhiteListEntry:
    """ entry of a type back/white list
    """

    def __init__(self, dictObj = None):

        #: entry of a type back/white list
        self.name = None

        #: entry of a type back/white list
        self.type = None
        if dictObj is not None:
            self.initFromDict(dictObj)

    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        self.name = dictObj.get('name', None)

        self.type = BlackWhiteListEntryTypeEnum.valueForString(dictObj.get('type', None))


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

    def __init__(self, dictObj = None):

        #: parameter of a code generation task that creates one file
        self.template = None

        #: parameter of a code generation task that creates one file
        self.destFile = None

        #: parameter of a code generation task that creates one file
        self.templateParams = []
        if dictObj is not None:
            self.initFromDict(dictObj)

    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        self.template = dictObj.get('template', None)

        self.destFile = dictObj.get('destFile', None)

        arrayTemplateParams = dictObj.get('templateParams', [])
        for elemTemplateParams in arrayTemplateParams:
            self.templateParams.append(
                TemplateParam(elemTemplateParams))


class TemplateParam:
    """ additional, template specific custom parameter for codegen task
    """

    def __init__(self, dictObj = None):

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
        if dictObj is not None:
            self.initFromDict(dictObj)

    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        self.name = dictObj.get('name', None)

        self.value = dictObj.get('value', None)

        arrayRequiredDomains = dictObj.get('requiredDomains', [])
        for elemRequiredDomains in arrayRequiredDomains:
            self.requiredDomains.append(elemRequiredDomains)

        arrayRequiredTags = dictObj.get('requiredTags', [])
        for elemRequiredTags in arrayRequiredTags:
            self.requiredTags.append(elemRequiredTags)

        arrayRequiredNames = dictObj.get('requiredNames', [])
        for elemRequiredNames in arrayRequiredNames:
            self.requiredNames.append(elemRequiredNames)


class MultiFileTask:
    """ parameter of a code generation task that creates one file per model type
    """

    def __init__(self, dictObj = None):

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
        if dictObj is not None:
            self.initFromDict(dictObj)

    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        self.template = dictObj.get('template', None)

        self.destDir = dictObj.get('destDir', None)

        self.destFilePrefix = dictObj.get('destFilePrefix', None)

        self.destFilePostfix = dictObj.get('destFilePostfix', None)

        self.destFileExt = dictObj.get('destFileExt', None)

        self.upperCaseStartedDestFileName = dictObj.get('upperCaseStartedDestFileName', False)

        self.fileFilterType = MultiFileTaskFileFilterTypeEnum.valueForString(dictObj.get('fileFilterType', None))

        arrayTemplateParams = dictObj.get('templateParams', [])
        for elemTemplateParams in arrayTemplateParams:
            self.templateParams.append(
                TemplateParam(elemTemplateParams))

        self.createOnlyIfNotExist = dictObj.get('createOnlyIfNotExist', False)

        self.createTmpFileIfAlreadyExist = dictObj.get('createTmpFileIfAlreadyExist', False)


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
    def __init__(self, dictObj = None):

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
        if dictObj is not None:
            self.initFromDict(dictObj)

    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        self.outputType = RandomDataTaskOutputTypeEnum.valueForString(dictObj.get('outputType', None))

        self.destDir = dictObj.get('destDir', None)

        self.defaultMinElemCount = dictObj.get('defaultMinElemCount', 1)

        self.defaultMaxElemCount = dictObj.get('defaultMaxElemCount', 10)

        arraySpecialElemCounts = dictObj.get('specialElemCounts', [])
        for elemSpecialElemCounts in arraySpecialElemCounts:
            self.specialElemCounts.append(
                RandomDataTaskSpecialElemCounts(elemSpecialElemCounts))

        arrayDefaultKeyPropNames = dictObj.get('defaultKeyPropNames', [])
        for elemDefaultKeyPropNames in arrayDefaultKeyPropNames:
            self.defaultKeyPropNames.append(elemDefaultKeyPropNames)

        arraySpecialKeyPropNames = dictObj.get('specialKeyPropNames', [])
        for elemSpecialKeyPropNames in arraySpecialKeyPropNames:
            self.specialKeyPropNames.append(
                RandomDataTaskSpecialKeyPropNames(elemSpecialKeyPropNames))

        arrayValuePools = dictObj.get('valuePools', [])
        for elemValuePools in arrayValuePools:
            self.valuePools.append(
                RandomDataTaskValuePools(elemValuePools))

        self.defaultMinSize = dictObj.get('defaultMinSize', 1)

        self.defaultMaxSize = dictObj.get('defaultMaxSize', 10)

        arraySpecialArraySizes = dictObj.get('specialArraySizes', [])
        for elemSpecialArraySizes in arraySpecialArraySizes:
            self.specialArraySizes.append(
                RandomDataTaskSpecialArraySizes(elemSpecialArraySizes))

        self.defaultMaxDepth = dictObj.get('defaultMaxDepth', 2)

        arraySpecialMaxDepths = dictObj.get('specialMaxDepths', [])
        for elemSpecialMaxDepths in arraySpecialMaxDepths:
            self.specialMaxDepths.append(
                RandomDataTaskSpecialMaxDepths(elemSpecialMaxDepths))


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
    def __init__(self, dictObj = None):

        self.typeName = None

        self.minElemCount = None

        self.maxElemCount = None
        if dictObj is not None:
            self.initFromDict(dictObj)

    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        self.typeName = dictObj.get('typeName', None)

        self.minElemCount = dictObj.get('minElemCount', None)

        self.maxElemCount = dictObj.get('maxElemCount', None)


class RandomDataTaskSpecialKeyPropNames:
    def __init__(self, dictObj = None):

        self.typeName = None

        self.keyPropName = None
        if dictObj is not None:
            self.initFromDict(dictObj)

    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        self.typeName = dictObj.get('typeName', None)

        self.keyPropName = dictObj.get('keyPropName', None)


class RandomDataTaskValuePools:
    def __init__(self, dictObj = None):

        self.propertyName = None

        self.useAll = False

        self.values = []
        if dictObj is not None:
            self.initFromDict(dictObj)

    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        self.propertyName = dictObj.get('propertyName', None)

        self.useAll = dictObj.get('useAll', False)

        arrayValues = dictObj.get('values', [])
        for elemValues in arrayValues:
            self.values.append(elemValues)


class RandomDataTaskSpecialArraySizes:
    def __init__(self, dictObj = None):

        self.propertyName = None

        self.minSize = None

        self.maxSize = None
        if dictObj is not None:
            self.initFromDict(dictObj)

    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        self.propertyName = dictObj.get('propertyName', None)

        self.minSize = dictObj.get('minSize', None)

        self.maxSize = dictObj.get('maxSize', None)


class RandomDataTaskSpecialMaxDepths:
    def __init__(self, dictObj = None):

        self.propertyName = None

        self.maxDepth = None
        if dictObj is not None:
            self.initFromDict(dictObj)

    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        self.propertyName = dictObj.get('propertyName', None)

        self.maxDepth = dictObj.get('maxDepth', None)


