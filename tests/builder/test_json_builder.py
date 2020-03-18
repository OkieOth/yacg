import unittest
import os.path
from yacg.builder.jsonBuilder import getModelFromJson


class TestJsonBuilder (unittest.TestCase):
    def testSingleTypeSchema(self):
        modelFile = 'resources/models/json/examples/single_type_schema.json'
        modelFileExists = os.path.isfile(modelFile)
        self.assertTrue ('model file exists: '+ modelFile,modelFileExists)
        modelTypes = getModelFromJson (modelFile)
        self.assertIsNotNone (modelTypes)
        self.assertEqual(2,len(modelTypes))

        mainType = None
        for type in modelTypes:
            if type.name == 'SingleTypeSchema':
                mainType = type

        self.assertIsNotNone (mainType)


if __name__ == '__main__':
    unittest.main()