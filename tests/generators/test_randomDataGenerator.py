import unittest
import os


from yacg.builder.jsonBuilder import getModelFromJson
from yacg.model.config import BlackWhiteListEntry, BlackWhiteListEntryTypeEnum
import yacg.generators.randomDataGenerator as randomDataGenerator
from yacg.model.config import RandomDataTask, RandomDataTaskOutputTypeEnum


import yacg.model.config as config


class TestRenderRandomData (unittest.TestCase):
    def testSimple(self):
        modelFile = 'tests/resources/models/json/examples/dummy_random_data_model.json'
        modelFileExists = os.path.isfile(modelFile)
        self.assertTrue('model file exists: ' + modelFile, modelFileExists)
        model = config.Model()
        model.schema = modelFile
        modelTypes = getModelFromJson(model, [])
        randomDataTask = RandomDataTask()
        randomDataTask.destDir = 'tmp/randomData1'
        randomDataTask.defaultKeyPropNames = ('id')
        randomDataTask.outputType = RandomDataTaskOutputTypeEnum.JSON

        randomData = randomDataGenerator.renderRandomData(modelTypes, [], [], randomDataTask)
        self.assertEqual(12, len(randomData))
        integerTypeData = randomData['IntegerType']
        self.assertTrue(len(integerTypeData) > 0)
        for d in integerTypeData:
            self.assertIsNotNone(d.get('guid', None))
        numberTypeData = randomData['NumberType']
        self.assertTrue(len(numberTypeData) > 0)
        for d in numberTypeData:
            self.assertIsNotNone(d.get('id', None))

    def testBlackList(self):
        modelFile = 'tests/resources/models/json/examples/dummy_random_data_model.json'
        modelFileExists = os.path.isfile(modelFile)
        self.assertTrue('model file exists: ' + modelFile, modelFileExists)
        model = config.Model()
        model.schema = modelFile
        modelTypes = getModelFromJson(model, [])
        randomDataTask = RandomDataTask()
        randomDataTask.destDir = 'tmp/randomData2'
        randomDataTask.defaultKeyPropNames = ('id')

        blackList = []
        blackListEntry = BlackWhiteListEntry()
        blackListEntry.name = 'BooleanType'
        blackListEntry.type = BlackWhiteListEntryTypeEnum.TYPE
        blackList.append(blackListEntry)
        blackListEntry = BlackWhiteListEntry()
        blackListEntry.name = 'StringType'
        blackListEntry.type = BlackWhiteListEntryTypeEnum.TYPE
        blackList.append(blackListEntry)
        blackListEntry = BlackWhiteListEntry()
        blackListEntry.name = 'Type'
        blackListEntry.type = BlackWhiteListEntryTypeEnum.TYPE
        blackList.append(blackListEntry)

        randomData = randomDataGenerator.renderRandomData(modelTypes, blackList, [], randomDataTask)
        self.assertEqual(9, len(randomData))
        integerTypeData = randomData['IntegerType']
        self.assertTrue(len(integerTypeData) > 0)
        for d in integerTypeData:
            self.assertIsNotNone(d.get('guid', None))
        numberTypeData = randomData['NumberType']
        self.assertTrue(len(numberTypeData) > 0)
        for d in numberTypeData:
            self.assertIsNotNone(d.get('id', None))

    def testWhiteList(self):
        modelFile = 'tests/resources/models/json/examples/dummy_random_data_model.json'
        modelFileExists = os.path.isfile(modelFile)
        self.assertTrue('model file exists: ' + modelFile, modelFileExists)
        model = config.Model()
        model.schema = modelFile
        modelTypes = getModelFromJson(model, [])
        randomDataTask = RandomDataTask()
        randomDataTask.destDir = 'tmp/randomData3'
        randomDataTask.defaultKeyPropNames = ('id')

        whiteList = []
        whiteListEntry = BlackWhiteListEntry()
        whiteListEntry.name = 'IntegerType'
        whiteListEntry.type = BlackWhiteListEntryTypeEnum.TYPE
        whiteList.append(whiteListEntry)
        whiteListEntry = BlackWhiteListEntry()
        whiteListEntry.name = 'NumberType'
        whiteListEntry.type = BlackWhiteListEntryTypeEnum.TYPE
        whiteList.append(whiteListEntry)

        randomData = randomDataGenerator.renderRandomData(modelTypes, [], whiteList, randomDataTask)
        self.assertEqual(2, len(randomData))
        integerTypeData = randomData['IntegerType']
        self.assertTrue(len(integerTypeData) > 0)
        for d in integerTypeData:
            self.assertIsNotNone(d.get('guid', None))
        numberTypeData = randomData['NumberType']
        self.assertTrue(len(numberTypeData) > 0)
        for d in numberTypeData:
            self.assertIsNotNone(d.get('id', None))

    def testWhiteList2(self):
        modelFile = 'tests/resources/models/json/examples/dummy_random_data_model.json'
        modelFileExists = os.path.isfile(modelFile)
        self.assertTrue('model file exists: ' + modelFile, modelFileExists)
        model = config.Model()
        model.schema = modelFile
        modelTypes = getModelFromJson(model, [])
        randomDataTask = RandomDataTask()
        randomDataTask.destDir = 'tmp/randomData4'
        randomDataTask.defaultKeyPropNames = ('id')

        whiteList = []
        whiteListEntry = BlackWhiteListEntry()
        whiteListEntry.name = 'ComplexType'
        whiteListEntry.type = BlackWhiteListEntryTypeEnum.TYPE
        whiteList.append(whiteListEntry)

        randomData = randomDataGenerator.renderRandomData(modelTypes, [], whiteList, randomDataTask)
        self.assertEqual(1, len(randomData))
