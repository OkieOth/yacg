import unittest
import os

import yacg.model.config as config
import yacg.generators.helper.generatorHelperFuncs as generatorHelper
from yacg.builder.jsonBuilder import getModelFromJson
from yacg.model.config import BlackWhiteListEntry, BlackWhiteListEntryTypeEnum
from yacg.generators.helper.filter.swaggerPathFilter import swaggerFilterByOperationId


class TestMultiFileCustomFilter (unittest.TestCase):
    def testGetPythonValueForTypeStringType(self):
        modelFile = 'tests/resources/models/json/examples/swagger_v2_example.json'
        modelFileExists = os.path.isfile(modelFile)
        self.assertTrue('model file exists: ' + modelFile, modelFileExists)
        model = config.Model()
        model.schema = modelFile
        ignorePathTypes = False
        modelTypes = getModelFromJson(model, [], ignorePathTypes)
        whiteList = []
        whiteListEntry = BlackWhiteListEntry()
        whiteListEntry.name = 'PathType'
        whiteListEntry.type = BlackWhiteListEntryTypeEnum.TYPETYPE
        whiteList.append(whiteListEntry)
        pathTypes = generatorHelper.trimModelTypes(modelTypes, (), whiteList)
        self.assertEqual(14, len(pathTypes))
        multiFileTypes = swaggerFilterByOperationId(pathTypes)
        self.assertEqual(20, len(multiFileTypes))
