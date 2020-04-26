import unittest
import os.path
from mako.template import Template
from yacg.builder.jsonBuilder import getModelFromJson

import yacg.model.config as config


class TestDictToObject (unittest.TestCase):
    def testDictToObj(self):
        # TODO
        modelFile = 'resources/models/json/yacg_config_schema.json'
        modelFileExists = os.path.isfile(modelFile)
        self.assertTrue('model file exists: ' + modelFile, modelFileExists)
        model = config.Model()
        model.schema = modelFile
        modelTypes = getModelFromJson(model, [])
        templateFile = 'resources/templates/pythonBeans.mako'
        template = Template(filename=templateFile)
        templateFileExists = os.path.isfile(modelFile)
        self.assertTrue('template file exists: ' + templateFile, templateFileExists)
        templateParameterDict = {}
        templateParameterDict['modelPackage'] = 'yacg.model.config'
        renderResult = template.render(modelTypes=modelTypes, templateParameters=templateParameterDict)
        self.assertIsNotNone(renderResult)

        testOutputFile = "tmp/config.py"
        f = open(testOutputFile, "w+")
        f.write(renderResult)
        f.close()

