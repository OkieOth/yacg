import unittest
import os.path

from yacg.util.fileUtils import getInternalTemplatePath


class TestFileUtils (unittest.TestCase):
    def testUpperCamelCase(self):
        modelFile = 'resources/models/json/config_schema.json'
        modelFileExists = os.path.isfile(modelFile)
        self.assertTrue(modelFileExists)

    def testFindTemplateFromScriptPos(self):
        currentPath = os.path.realpath(__file__)
        lastSlash = currentPath.rindex('/')
        templateFile = currentPath[:lastSlash] + '/../../yacg/generators/templates/plantUml.mako'
        fileExists = os.path.exists(templateFile)
        self.assertTrue(fileExists)

    def testGetInternalTemplatePath(self):
        templateFile = getInternalTemplatePath('generators/templates/plantUml.mako')
        fileExists = os.path.exists(templateFile)
        self.assertTrue(fileExists)

