# Attention, this file is generated. Manual changes get lost with the next
# run of the code generation.
# created by yacg (template: pythonBeans.mako v1.0.0)

from enum import Enum


class Job:
    """base object that describes a complete code generation process
    """

    def __init__(self, dictObj=None):

        #: a short identifier of that job
        self.name = None

        #: some words to explain
        self.description = None

        #: list of models used for that job
        self.models = []

        #: list of tasks that should run
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
    """A model that should be used
    """

    def __init__(self, dictObj=None):

        #: path to the jsonSchema file, entry can also contain env vars in the format '{ENV_VAR_NAME}'
        self.schema = None

        #: optional nameSpace string for the model, if not set the file name/path are used as namespace
        self.domain = None

        #: what elements should be excluded from handling
        self.blackListed = []

        #: what elements should be included in the handling
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
    """A task to run
    """

    def __init__(self, dictObj=None):

        #: short visual identifier
        self.name = None

        #: some words to explain
        self.description = None

        #: what elements should be excluded from handling
        self.blackListed = []

        #: what elements should be included in the handling
        self.whiteListed = []

        #: the code generation creates only one file
        self.singleFileTask = None

        #: the code generation creates one file per type
        self.multiFileTask = None

        #: the code generation creates one file per type with random data
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

        subDictObj = dictObj.get('singleFileTask', None)
        if subDictObj is not None:
            self.singleFileTask = SingleFileTask(subDictObj)

        subDictObj = dictObj.get('multiFileTask', None)
        if subDictObj is not None:
            self.multiFileTask = MultiFileTask(subDictObj)

        subDictObj = dictObj.get('randomDataTask', None)
        if subDictObj is not None:
            self.randomDataTask = RandomDataTask(subDictObj)


class BlackWhiteListEntry:
    """entry of a type back/white list
    """

    def __init__(self, dictObj=None):

        #: name that should be in-/excluded
        self.name = None

        #: how is the name to be interpreted. If type is missing, then 'type' is expected
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
    """parameter of a code generation task that creates one file
    """

    def __init__(self, dictObj=None):

        #: template to use for that task, either the name of a built in template, or a file system path, entry can also contain env vars in the format '{ENV_VAR_NAME}'
        self.template = None

        #: name and path for the file to create, entry can also contain env vars in the format '{ENV_VAR_NAME}'
        self.destFile = None

        #: custom parameter that are passed to the template, while it is processed
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
    """additional, template specific custom parameter for codegen task
    """

    def __init__(self, dictObj=None):

        #: name of the custom parameter
        self.name = None

        #: value of the custom parameter
        self.value = None

        #: if set then this parameter only effected types of the specific domains
        self.requiredDomains = []

        #: if set then this parameter only effected types or attributes with the specific tag
        self.requiredTags = []

        #: if set then this parameter only effected types or attributes with the specific name
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
    """parameter of a code generation task that creates one file per model type
    """

    def __init__(self, dictObj=None):

        #: template to use for that task, either the name of a built in template, or a file system path, entry can also contain env vars in the format '{ENV_VAR_NAME}'
        self.template = None

        #: path where the files will be created, entry can also contain env vars in the format '{ENV_VAR_NAME}'
        self.destDir = None

        #: prefix for the name of the created files
        self.destFilePrefix = None

        #: postfix for the name of the created files
        self.destFilePostfix = None

        #: file extention for the created files
        self.destFileExt = None

        #: the name of the destination file should start with an upper case
        self.upperCaseStartedDestFileName = False

        #: this defines how the model is splitted to create the multiple files
        self.fileFilterType = MultiFileTaskFileFilterTypeEnum.TYPE

        #: custom parameter that are passed to the template, while it is processed
        self.templateParams = []

        #: create the new file only if it not already exists
        self.createOnlyIfNotExist = False

        #: instead of creation of the orininal file it will be created with a '.tmp' extention, if the file aleady exists
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
    def __init__(self, dictObj=None):

        self.outputType = None

        #: path where the files will be created, entry can also contain env vars in the format '{ENV_VAR_NAME}'
        self.destDir = None

        #: minimum number of elements that should be created for all types
        self.defaultMinElemCount = 1

        #: maximum number of elements that should be created for all types
        self.defaultMaxElemCount = 10

        self.specialElemCounts = []

        #: list of names for primary key fields in the model
        self.defaultKeyPropNames = []

        self.specialKeyPropNames = []

        self.valuePools = []

        #: minimum size of arrays
        self.defaultMinSize = 1

        #: maximum size of arrays
        self.defaultMaxSize = 10

        self.specialArraySizes = []

        #: default max level depth when generating object trees
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
    def __init__(self, dictObj=None):

        #: TYPENAME
        self.typeName = None

        #: how many elements should be generated for that type at minimum
        self.minElemCount = None

        #: how many elements should be generated for that type at maximum
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
    def __init__(self, dictObj=None):

        #: TYPENAME
        self.typeName = None

        #: name of the attribute that represents the key for that type
        self.keyPropName = None

        if dictObj is not None:
            self.initFromDict(dictObj)

    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        self.typeName = dictObj.get('typeName', None)

        self.keyPropName = dictObj.get('keyPropName', None)


class RandomDataTaskValuePools:
    def __init__(self, dictObj=None):

        #: TYPENAME.PROPERTYNAME
        self.propertyName = None

        #: should all values from the pool be used in the data gen
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
    def __init__(self, dictObj=None):

        #: TYPENAME.PROPERTYNAME
        self.propertyName = None

        #: how many array elements should be generated for that attrib, at minimum
        self.minSize = None

        #: how many array elements should be generated for that attrib, at maximum
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
    def __init__(self, dictObj=None):

        #: TYPENAME.PROPERTYNAME
        self.propertyName = None

        #: max level depth when generating object trees for that attrib
        self.maxDepth = None

        if dictObj is not None:
            self.initFromDict(dictObj)

    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        self.propertyName = dictObj.get('propertyName', None)

        self.maxDepth = dictObj.get('maxDepth', None)


