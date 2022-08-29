import unittest
import os.path

from yacg.util.fileUtils import getInternalTemplatePath, getDirName


class TestFileUtils (unittest.TestCase):
    def testUpperCamelCase(self):
        modelFile = 'resources/models/json/yacg_config_schema.json'
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

    def testGetDirName(self):
        self.assertEqual(getDirName('test'), (''))
        self.assertEqual(getDirName('/test'), (''))
        self.assertEqual(getDirName('test/xxx.y'), ('test'))
        self.assertEqual(getDirName('/test/o'), ('/test'))
        self.assertEqual(getDirName('aaa/test/xxx.y'), ('aaa/test'))
        self.assertEqual(getDirName('/something/test/o'), ('/something/test'))

