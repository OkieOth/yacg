import unittest
import os.path
from mako.template import Template
from yacg.builder.jsonBuilder import getModelFromJson

import yacg.model.config as config


class TestOpenApi (unittest.TestCase):
    def testYacgModel(self):
        modelFile = 'resources/models/json/yacg_model_schema.json'
        modelFileExists = os.path.isfile(modelFile)
        self.assertTrue('model file exists: ' + modelFile, modelFileExists)
        model = config.Model()
        model.schema = modelFile
        modelTypes = getModelFromJson(model, [])
        templateFile = 'resources/templates/examples/openApiJson.mako'
        template = Template(filename=templateFile)
        templateFileExists = os.path.isfile(modelFile)
        self.assertTrue('template file exists: ' + templateFile, templateFileExists)
        templateParameters = {}
        templateParameters['restTypes'] = 'ComplexType,Tag'
        renderResult = template.render(modelTypes=modelTypes, templateParameters=templateParameters)
        self.assertIsNotNone(renderResult)

        testOutputFile = "tmp/yacgModelOpenApi.json"
        f = open(testOutputFile, "w+")
        f.write(renderResult)
        f.close()
