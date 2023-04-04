# Attention, this file is generated. Manual changes get lost with the next
# run of the code generation.
# created by yacg (template: pythonBeans.mako v1.1.0)

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
            d = vars(dictObj) if not isinstance(dictObj, dict) else dictObj
            self.initFromDict(d)

    def toDict(self):
        ret = {}
        if self.name is not None:
            ret["name"] = self.name
        if self.description is not None:
            ret["description"] = self.description
        if (self.models is not None) and (len(self.models) > 0):
            ret["models"] = self.models.toDict()
        if (self.tasks is not None) and (len(self.tasks) > 0):
            ret["tasks"] = self.tasks.toDict()
        return ret

    @classmethod
    def initWithFlatValue(cls, attribName, value, initObj = None):
        ret = initObj
        if attribName == "name":
            if ret is None:
                ret = Job()
            ret.name = value
        if attribName == "description":
            if ret is None:
                ret = Job()
            ret.description = value
        initObj = ret.models if ret is not None else None
        modelsTmp = Model.initWithFlatValue(attribName, value, initObj)
        if modelsTmp is not None:
            if ret is None:
                ret = Job()
            ret.models = modelsTmp
        initObj = ret.tasks if ret is not None else None
        tasksTmp = Task.initWithFlatValue(attribName, value, initObj)
        if tasksTmp is not None:
            if ret is None:
                ret = Job()
            ret.tasks = tasksTmp
        return ret

    @classmethod
    def createFromFlatDict(cls, flatDict={}):
        ret = None
        for key, value in flatDict.items():
            if key == "name":
                if ret is None:
                    ret = Job()
                ret.name = value
            if key == "description":
                if ret is None:
                    ret = Job()
                ret.description = value
            initObj = ret.models if ret is not None else None
            modelsTmp = Model.initWithFlatValue(attribName, value, initObj)
            if modelsTmp is not None:
                if ret is None:
                    ret = Job()
                ret.models = modelsTmp
            initObj = ret.tasks if ret is not None else None
            tasksTmp = Task.initWithFlatValue(attribName, value, initObj)
            if tasksTmp is not None:
                if ret is None:
                    ret = Job()
                ret.tasks = tasksTmp
        return ret

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
            d = vars(dictObj) if not isinstance(dictObj, dict) else dictObj
            self.initFromDict(d)

    def toDict(self):
        ret = {}
        if self.schema is not None:
            ret["schema"] = self.schema
        if self.domain is not None:
            ret["domain"] = self.domain
        if (self.blackListed is not None) and (len(self.blackListed) > 0):
            ret["blackListed"] = self.blackListed.toDict()
        if (self.whiteListed is not None) and (len(self.whiteListed) > 0):
            ret["whiteListed"] = self.whiteListed.toDict()
        return ret

    @classmethod
    def initWithFlatValue(cls, attribName, value, initObj = None):
        ret = initObj
        if attribName == "schema":
            if ret is None:
                ret = Model()
            ret.schema = value
        if attribName == "domain":
            if ret is None:
                ret = Model()
            ret.domain = value
        initObj = ret.blackListed if ret is not None else None
        blackListedTmp = BlackWhiteListEntry.initWithFlatValue(attribName, value, initObj)
        if blackListedTmp is not None:
            if ret is None:
                ret = Model()
            ret.blackListed = blackListedTmp
        initObj = ret.whiteListed if ret is not None else None
        whiteListedTmp = BlackWhiteListEntry.initWithFlatValue(attribName, value, initObj)
        if whiteListedTmp is not None:
            if ret is None:
                ret = Model()
            ret.whiteListed = whiteListedTmp
        return ret

    @classmethod
    def createFromFlatDict(cls, flatDict={}):
        ret = None
        for key, value in flatDict.items():
            if key == "schema":
                if ret is None:
                    ret = Model()
                ret.schema = value
            if key == "domain":
                if ret is None:
                    ret = Model()
                ret.domain = value
            initObj = ret.blackListed if ret is not None else None
            blackListedTmp = BlackWhiteListEntry.initWithFlatValue(attribName, value, initObj)
            if blackListedTmp is not None:
                if ret is None:
                    ret = Model()
                ret.blackListed = blackListedTmp
            initObj = ret.whiteListed if ret is not None else None
            whiteListedTmp = BlackWhiteListEntry.initWithFlatValue(attribName, value, initObj)
            if whiteListedTmp is not None:
                if ret is None:
                    ret = Model()
                ret.whiteListed = whiteListedTmp
        return ret

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

        if dictObj is not None:
            d = vars(dictObj) if not isinstance(dictObj, dict) else dictObj
            self.initFromDict(d)

    def toDict(self):
        ret = {}
        if self.name is not None:
            ret["name"] = self.name
        if self.description is not None:
            ret["description"] = self.description
        if (self.blackListed is not None) and (len(self.blackListed) > 0):
            ret["blackListed"] = self.blackListed.toDict()
        if (self.whiteListed is not None) and (len(self.whiteListed) > 0):
            ret["whiteListed"] = self.whiteListed.toDict()
        if self.singleFileTask is not None:
            ret["singleFileTask"] = self.singleFileTask.toDict()
        if self.multiFileTask is not None:
            ret["multiFileTask"] = self.multiFileTask.toDict()
        return ret

    @classmethod
    def initWithFlatValue(cls, attribName, value, initObj = None):
        ret = initObj
        if attribName == "name":
            if ret is None:
                ret = Task()
            ret.name = value
        if attribName == "description":
            if ret is None:
                ret = Task()
            ret.description = value
        initObj = ret.blackListed if ret is not None else None
        blackListedTmp = BlackWhiteListEntry.initWithFlatValue(attribName, value, initObj)
        if blackListedTmp is not None:
            if ret is None:
                ret = Task()
            ret.blackListed = blackListedTmp
        initObj = ret.whiteListed if ret is not None else None
        whiteListedTmp = BlackWhiteListEntry.initWithFlatValue(attribName, value, initObj)
        if whiteListedTmp is not None:
            if ret is None:
                ret = Task()
            ret.whiteListed = whiteListedTmp
        initObj = ret.singleFileTask if ret is not None else None
        singleFileTaskTmp = SingleFileTask.initWithFlatValue(attribName, value, initObj)
        if singleFileTaskTmp is not None:
            if ret is None:
                ret = Task()
            ret.singleFileTask = singleFileTaskTmp
        initObj = ret.multiFileTask if ret is not None else None
        multiFileTaskTmp = MultiFileTask.initWithFlatValue(attribName, value, initObj)
        if multiFileTaskTmp is not None:
            if ret is None:
                ret = Task()
            ret.multiFileTask = multiFileTaskTmp
        return ret

    @classmethod
    def createFromFlatDict(cls, flatDict={}):
        ret = None
        for key, value in flatDict.items():
            if key == "name":
                if ret is None:
                    ret = Task()
                ret.name = value
            if key == "description":
                if ret is None:
                    ret = Task()
                ret.description = value
            initObj = ret.blackListed if ret is not None else None
            blackListedTmp = BlackWhiteListEntry.initWithFlatValue(attribName, value, initObj)
            if blackListedTmp is not None:
                if ret is None:
                    ret = Task()
                ret.blackListed = blackListedTmp
            initObj = ret.whiteListed if ret is not None else None
            whiteListedTmp = BlackWhiteListEntry.initWithFlatValue(attribName, value, initObj)
            if whiteListedTmp is not None:
                if ret is None:
                    ret = Task()
                ret.whiteListed = whiteListedTmp
            initObj = ret.singleFileTask if ret is not None else None
            singleFileTaskTmp = SingleFileTask.initWithFlatValue(attribName, value, initObj)
            if singleFileTaskTmp is not None:
                if ret is None:
                    ret = Task()
                ret.singleFileTask = singleFileTaskTmp
            initObj = ret.multiFileTask if ret is not None else None
            multiFileTaskTmp = MultiFileTask.initWithFlatValue(attribName, value, initObj)
            if multiFileTaskTmp is not None:
                if ret is None:
                    ret = Task()
                ret.multiFileTask = multiFileTaskTmp
        return ret

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


class BlackWhiteListEntry:
    """entry of a type back/white list
    """

    def __init__(self, dictObj=None):

        #: name that should be in-/excluded
        self.name = None

        #: how is the name to be interpreted. If type is missing, then 'type' is expected
        self.type = None

        if dictObj is not None:
            d = vars(dictObj) if not isinstance(dictObj, dict) else dictObj
            self.initFromDict(d)

    def toDict(self):
        ret = {}
        if self.name is not None:
            ret["name"] = self.name
        if self.type is not None:
            ret["type"] = BlackWhiteListEntryTypeEnum.valueAsString(self.type)
        return ret

    @classmethod
    def initWithFlatValue(cls, attribName, value, initObj = None):
        ret = initObj
        if attribName == "name":
            if ret is None:
                ret = BlackWhiteListEntry()
            ret.name = value
        if attribName == "type":
            if ret is None:
                ret = BlackWhiteListEntry()
            ret.type = BlackWhiteListEntryTypeEnum.valueForString(value)
        return ret

    @classmethod
    def createFromFlatDict(cls, flatDict={}):
        ret = None
        for key, value in flatDict.items():
            if key == "name":
                if ret is None:
                    ret = BlackWhiteListEntry()
                ret.name = value
            if key == "type":
                if ret is None:
                    ret = BlackWhiteListEntry()
                ret.type = BlackWhiteListEntryTypeEnum.valueForString(value)
        return ret

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
            d = vars(dictObj) if not isinstance(dictObj, dict) else dictObj
            self.initFromDict(d)

    def toDict(self):
        ret = {}
        if self.template is not None:
            ret["template"] = self.template
        if self.destFile is not None:
            ret["destFile"] = self.destFile
        if (self.templateParams is not None) and (len(self.templateParams) > 0):
            ret["templateParams"] = self.templateParams.toDict()
        return ret

    @classmethod
    def initWithFlatValue(cls, attribName, value, initObj = None):
        ret = initObj
        if attribName == "template":
            if ret is None:
                ret = SingleFileTask()
            ret.template = value
        if attribName == "destFile":
            if ret is None:
                ret = SingleFileTask()
            ret.destFile = value
        initObj = ret.templateParams if ret is not None else None
        templateParamsTmp = TemplateParam.initWithFlatValue(attribName, value, initObj)
        if templateParamsTmp is not None:
            if ret is None:
                ret = SingleFileTask()
            ret.templateParams = templateParamsTmp
        return ret

    @classmethod
    def createFromFlatDict(cls, flatDict={}):
        ret = None
        for key, value in flatDict.items():
            if key == "template":
                if ret is None:
                    ret = SingleFileTask()
                ret.template = value
            if key == "destFile":
                if ret is None:
                    ret = SingleFileTask()
                ret.destFile = value
            initObj = ret.templateParams if ret is not None else None
            templateParamsTmp = TemplateParam.initWithFlatValue(attribName, value, initObj)
            if templateParamsTmp is not None:
                if ret is None:
                    ret = SingleFileTask()
                ret.templateParams = templateParamsTmp
        return ret

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
            d = vars(dictObj) if not isinstance(dictObj, dict) else dictObj
            self.initFromDict(d)

    def toDict(self):
        ret = {}
        if self.name is not None:
            ret["name"] = self.name
        if self.value is not None:
            ret["value"] = self.value
        if (self.requiredDomains is not None) and (len(self.requiredDomains) > 0):
            ret["requiredDomains"] = self.requiredDomains
        if (self.requiredTags is not None) and (len(self.requiredTags) > 0):
            ret["requiredTags"] = self.requiredTags
        if (self.requiredNames is not None) and (len(self.requiredNames) > 0):
            ret["requiredNames"] = self.requiredNames
        return ret

    @classmethod
    def initWithFlatValue(cls, attribName, value, initObj = None):
        ret = initObj
        if attribName == "name":
            if ret is None:
                ret = TemplateParam()
            ret.name = value
        if attribName == "value":
            if ret is None:
                ret = TemplateParam()
            ret.value = value
        if attribName == "requiredDomains":
            if ret is None:
                ret = TemplateParam()
            ret.requiredDomains = value
        if attribName == "requiredTags":
            if ret is None:
                ret = TemplateParam()
            ret.requiredTags = value
        if attribName == "requiredNames":
            if ret is None:
                ret = TemplateParam()
            ret.requiredNames = value
        return ret

    @classmethod
    def createFromFlatDict(cls, flatDict={}):
        ret = None
        for key, value in flatDict.items():
            if key == "name":
                if ret is None:
                    ret = TemplateParam()
                ret.name = value
            if key == "value":
                if ret is None:
                    ret = TemplateParam()
                ret.value = value
            if key == "requiredDomains":
                if ret is None:
                    ret = TemplateParam()
                ret.requiredDomains = value
            if key == "requiredTags":
                if ret is None:
                    ret = TemplateParam()
                ret.requiredTags = value
            if key == "requiredNames":
                if ret is None:
                    ret = TemplateParam()
                ret.requiredNames = value
        return ret

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
            d = vars(dictObj) if not isinstance(dictObj, dict) else dictObj
            self.initFromDict(d)

    def toDict(self):
        ret = {}
        if self.template is not None:
            ret["template"] = self.template
        if self.destDir is not None:
            ret["destDir"] = self.destDir
        if self.destFilePrefix is not None:
            ret["destFilePrefix"] = self.destFilePrefix
        if self.destFilePostfix is not None:
            ret["destFilePostfix"] = self.destFilePostfix
        if self.destFileExt is not None:
            ret["destFileExt"] = self.destFileExt
        if self.upperCaseStartedDestFileName is not None:
            ret["upperCaseStartedDestFileName"] = self.upperCaseStartedDestFileName
        if self.fileFilterType is not None:
            ret["fileFilterType"] = MultiFileTaskFileFilterTypeEnum.valueAsString(self.fileFilterType)
        if (self.templateParams is not None) and (len(self.templateParams) > 0):
            ret["templateParams"] = self.templateParams.toDict()
        if self.createOnlyIfNotExist is not None:
            ret["createOnlyIfNotExist"] = self.createOnlyIfNotExist
        if self.createTmpFileIfAlreadyExist is not None:
            ret["createTmpFileIfAlreadyExist"] = self.createTmpFileIfAlreadyExist
        return ret

    @classmethod
    def initWithFlatValue(cls, attribName, value, initObj = None):
        ret = initObj
        if attribName == "template":
            if ret is None:
                ret = MultiFileTask()
            ret.template = value
        if attribName == "destDir":
            if ret is None:
                ret = MultiFileTask()
            ret.destDir = value
        if attribName == "destFilePrefix":
            if ret is None:
                ret = MultiFileTask()
            ret.destFilePrefix = value
        if attribName == "destFilePostfix":
            if ret is None:
                ret = MultiFileTask()
            ret.destFilePostfix = value
        if attribName == "destFileExt":
            if ret is None:
                ret = MultiFileTask()
            ret.destFileExt = value
        if attribName == "upperCaseStartedDestFileName":
            if ret is None:
                ret = MultiFileTask()
            ret.upperCaseStartedDestFileName = value
        if attribName == "fileFilterType":
            if ret is None:
                ret = MultiFileTask()
            ret.fileFilterType = MultiFileTaskFileFilterTypeEnum.valueForString(value)
        initObj = ret.templateParams if ret is not None else None
        templateParamsTmp = TemplateParam.initWithFlatValue(attribName, value, initObj)
        if templateParamsTmp is not None:
            if ret is None:
                ret = MultiFileTask()
            ret.templateParams = templateParamsTmp
        if attribName == "createOnlyIfNotExist":
            if ret is None:
                ret = MultiFileTask()
            ret.createOnlyIfNotExist = value
        if attribName == "createTmpFileIfAlreadyExist":
            if ret is None:
                ret = MultiFileTask()
            ret.createTmpFileIfAlreadyExist = value
        return ret

    @classmethod
    def createFromFlatDict(cls, flatDict={}):
        ret = None
        for key, value in flatDict.items():
            if key == "template":
                if ret is None:
                    ret = MultiFileTask()
                ret.template = value
            if key == "destDir":
                if ret is None:
                    ret = MultiFileTask()
                ret.destDir = value
            if key == "destFilePrefix":
                if ret is None:
                    ret = MultiFileTask()
                ret.destFilePrefix = value
            if key == "destFilePostfix":
                if ret is None:
                    ret = MultiFileTask()
                ret.destFilePostfix = value
            if key == "destFileExt":
                if ret is None:
                    ret = MultiFileTask()
                ret.destFileExt = value
            if key == "upperCaseStartedDestFileName":
                if ret is None:
                    ret = MultiFileTask()
                ret.upperCaseStartedDestFileName = value
            if key == "fileFilterType":
                if ret is None:
                    ret = MultiFileTask()
                ret.fileFilterType = MultiFileTaskFileFilterTypeEnum.valueForString(value)
            initObj = ret.templateParams if ret is not None else None
            templateParamsTmp = TemplateParam.initWithFlatValue(attribName, value, initObj)
            if templateParamsTmp is not None:
                if ret is None:
                    ret = MultiFileTask()
                ret.templateParams = templateParamsTmp
            if key == "createOnlyIfNotExist":
                if ret is None:
                    ret = MultiFileTask()
                ret.createOnlyIfNotExist = value
            if key == "createTmpFileIfAlreadyExist":
                if ret is None:
                    ret = MultiFileTask()
                ret.createTmpFileIfAlreadyExist = value
        return ret

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



