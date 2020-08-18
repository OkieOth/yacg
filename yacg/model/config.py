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
        obj = Job()

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
        obj = Model()

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

    @classmethod
    def dictToObject(cls, dict):
        if dict is None:
            return None
        obj = Task()

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
        obj = BlackWhiteListEntry()

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
        obj = SingleFileTask()

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
        obj = TemplateParam()

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

    @classmethod
    def dictToObject(cls, dict):
        if dict is None:
            return None
        obj = MultiFileTask()

        obj.template = dict.get('template', None)

        obj.destDir = dict.get('destDir', None)

        obj.destFilePrefix = dict.get('destFilePrefix', None)

        obj.destFilePostfix = dict.get('destFilePostfix', None)

        obj.destFileExt = dict.get('destFileExt', None)

        obj.upperCaseStartedDestFileName = dict.get('upperCaseStartedDestFileName', None)

        obj.fileFilterType = MultiFileTaskFileFilterTypeEnum.valueForString(dict.get('fileFilterType', None))

        arrayTemplateParams = dict.get('templateParams', [])
        for elemTemplateParams in arrayTemplateParams:
            obj.templateParams.append(
                TemplateParam.dictToObject(elemTemplateParams))
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



