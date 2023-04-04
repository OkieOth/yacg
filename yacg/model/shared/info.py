# Attention, this file is generated. Manual changes get lost with the next
# run of the code generation.
# created by yacg (template: pythonBeans.mako v1.1.0)

import yacg.model.shared.info


class InfoSection:
    """Info section for API definition specs as openapi and ayncapi
    """

    def __init__(self, dictObj=None):
        self.title = None
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

    @classmethod
    def initWithFlatValue(cls, attribName, value, initObj = None):
        ret = initObj
        if attribName == "title":
            if ret is None:
                ret = InfoSection()
            ret.title = value
        if attribName == "version":
            if ret is None:
                ret = InfoSection()
            ret.version = value
        if attribName == "description":
            if ret is None:
                ret = InfoSection()
            ret.description = value
        if attribName == "license":
            if ret is None:
                ret = InfoSection()
            ret.license = value
        return ret

    @classmethod
    def createFromFlatDict(cls, flatDict={}):
        ret = None
        for key, value in flatDict.items():
            if key == "title":
                if ret is None:
                    ret = InfoSection()
                ret.title = value
            if key == "version":
                if ret is None:
                    ret = InfoSection()
                ret.version = value
            if key == "description":
                if ret is None:
                    ret = InfoSection()
                ret.description = value
            if key == "license":
                if ret is None:
                    ret = InfoSection()
                ret.license = value
        return ret

    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        self.title = dictObj.get('title', None)

        self.version = dictObj.get('version', None)

        self.description = dictObj.get('description', None)

        self.license = dictObj.get('license', None)


