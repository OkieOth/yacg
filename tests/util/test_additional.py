import unittest
import os.path
from yacg.builder.jsonBuilder import getModelFromJson
import yacg.model.config as config
import yacg.model.modelFuncs as modelFuncs


class TestAdditional (unittest.TestCase):
    def testFlattenTypes(self):
        modelFile = 'tests/resources/models/json/examples/more_sophisticated_allof.json'
        modelFileExists = os.path.isfile(modelFile)
        self.assertTrue('model file exists: ' + modelFile, modelFileExists)
        model = config.Model()
        model.schema = modelFile
        modelTypes = getModelFromJson(model, [])
        self.assertIsNotNone(modelTypes)
        self.assertEqual(7, len(modelTypes))
        for t in modelTypes:
            if t.name == 'MoreSophisticatedAllOf':
                self.assertEqual(1, len(t.properties))
                self.assertIsNotNone(t.extendsType)
            if t.name == 'Address':
                self.assertEqual(3, len(t.properties))
                self.assertIsNone(t.extendsType)
            if t.name == 'MainAdress':
                self.assertEqual(2, len(t.properties))
                self.assertIsNotNone(t.extendsType)
            if t.name == 'SimpleAllOfSchema':
                self.assertEqual(1, len(t.properties))
                self.assertIsNotNone(t.extendsType)
            if t.name == 'MainAddressComplex':
                self.assertEqual(3, len(t.properties))
                self.assertIsNone(t.extendsType)

        flattenTypes = modelFuncs.flattenTypes(modelTypes)
        self.assertIsNotNone(flattenTypes)
        self.assertEqual(7, len(flattenTypes))
        for t in flattenTypes:
            if t.name == 'MoreSophisticatedAllOf':
                self.assertEqual(4, len(t.properties))
                self.assertIsNone(t.extendsType)
            if t.name == 'Address':
                self.assertEqual(3, len(t.properties))
                self.assertIsNone(t.extendsType)
            if t.name == 'MainAdress':
                self.assertEqual(6, len(t.properties))
                self.assertIsNone(t.extendsType)
            if t.name == 'SimpleAllOfSchema':
                self.assertEqual(4, len(t.properties))
                self.assertIsNone(t.extendsType)
            if t.name == 'MainAddressComplex':
                self.assertEqual(3, len(t.properties))
                self.assertIsNone(t.extendsType)


