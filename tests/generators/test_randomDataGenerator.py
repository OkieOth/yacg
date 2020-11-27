import unittest
import os


from yacg.builder.jsonBuilder import getModelFromJson
import yacg.generators.randomDataGenerator as randomDataGenerator
from yacg.model.config import RandomDataTask


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
        randomDataTask.destDir = 'tmp/randomData'
        randomDataTask.defaultKeyPropNames = ('id')
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
