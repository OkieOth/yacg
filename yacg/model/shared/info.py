# Attention, this file is generated. Manual changes get lost with the next
# run of the code generation.
# created by yacg (template: pythonBeans.mako v1.1.0)

import yacg.model.shared.info


class InfoSection:
    """Info section for API definition specs as openapi and ayncapi
    """

    def __init__(self, dictObj=None):

        #: title of the model
        self.title = None

        #: version of the model
        self.version = None
        self.description = None
        self.license = None

        if dictObj is not None:
            d = vars(dictObj) if not isinstance(dictObj, dict) else dictObj
            self.initFromDict(d)

    def toDict(self):
        ret = {}
        if self.title is not None:
            ret["title"] = self.title
        if self.version is not None:
            ret["version"] = self.version
        if self.description is not None:
            ret["description"] = self.description
        if self.license is not None:
            ret["license"] = self.license
        return ret


    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        self.title = dictObj.get('title', None)

        self.version = dictObj.get('version', None)

        self.description = dictObj.get('description', None)

        self.license = dictObj.get('license', None)


