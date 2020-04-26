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
        obj = Job()
        obj.name = dict.get('name', None)
        obj.description = dict.get('description', None)
        
        for elemDict in dict.get('models', []):
            newObj = Model.dictToObj(elemDict)
            obj.models.append(newObj)
        for elem in dict.get('tasks', []):
            newObj = Task.dictToObj(elemDict)
            obj.tasks.append(newObj)
            
        return obj

    def objectToDict(self, dict):
        pass


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


class BlackWhiteListEntry:
    """ entry of a type back/white list
    """

    def __init__(self):

        #: entry of a type back/white list
        self.name = None

        #: entry of a type back/white list
        self.type = None


class BlackWhiteListEntryTypeEnum(Enum):
    TYPE = 'type'
    TAG = 'tag'
    CONTAINEDATTRIB = 'containedAttrib'
    NOTCONTAINEDATTRIB = 'notContainedAttrib'
    DOMAIN = 'domain'


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
        self.templateParams = []


