import unittest
import os.path


class TestFileUtils (unittest.TestCase):
    def testUpperCamelCase(self):
        modelFile = 'resources/models/json/config_schema.json'
        modelFileExists = os.path.isfile(modelFile)
        self.assertTrue ('model file exists: '+ modelFile,modelFileExists)
        print (os.path.abspath(modelFile))

       

