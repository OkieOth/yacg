import unittest
import os.path
from mako.template import Template
from yacg.builder.jsonBuilder import getModelFromJson

import yacg.model.config as config


class TestPlantUml (unittest.TestCase):
    def testSampleConfigSchema(self):
        modelFile = 'resources/models/json/yacg_config_schema.json'
        modelFileExists = os.path.isfile(modelFile)
        self.assertTrue('model file exists: ' + modelFile, modelFileExists)
        model = config.Model()
        model.schema = modelFile
        modelTypes = getModelFromJson(model, [])
        templateFile = 'resources/templates/examples/opc_test.mako'
        template = Template(filename=templateFile)
        templateFileExists = os.path.isfile(modelFile)
        self.assertTrue('template file exists: ' + templateFile, templateFileExists)
        renderResult = template.render(modelTypes=modelTypes)
        self.assertIsNotNone(renderResult)

        testOutputFile = "tmp/opc_test.xml"
        f = open(testOutputFile, "w+")
        f.write(renderResult)
        f.close()

