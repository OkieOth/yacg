# Attention, this file is generated. Manual changes get lost with the next
# run of the code generation.
# created by yacg (template: pythonBeans.mako v1.0.0)

import yacg.model.shared.info


class InfoSection:
    """ Info section for API definition specs as openapi and ayncapi
    """

    def __init__(self, dictObj=None):

        self.title = None

        self.version = None

        self.description = None

        self.license = None

        if dictObj is not None:
            self.initFromDict(dictObj)

    def initFromDict(self, dictObj):
        if dictObj is None:
            return

        self.title = dictObj.get('title', None)

        self.version = dictObj.get('version', None)

        self.description = dictObj.get('description', None)

        self.license = dictObj.get('license', None)


