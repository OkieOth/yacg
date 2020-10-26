import unittest
import os.path
from mako.template import Template
from yacg.builder.jsonBuilder import getModelFromJson

import yacg.model.config as config


class TestXsd (unittest.TestCase):
    def testSingleTypeSchema(self):
        modelFile = 'tests/resources/models/json/examples/single_type_schema.json'
        modelFileExists = os.path.isfile(modelFile)
        self.assertTrue('model file exists: ' + modelFile, modelFileExists)
        model = config.Model()
        model.schema = modelFile
        modelTypes = getModelFromJson(model, [])
        templateFile = 'yacg/generators/templates/xsd.mako'
        template = Template(filename=templateFile)
        templateFileExists = os.path.isfile(modelFile)
        self.assertTrue('template file exists: ' + templateFile, templateFileExists)
        renderResult = template.render(modelTypes=modelTypes, templateParameters={})
        self.assertIsNotNone(renderResult)

        testOutputFile = "tmp/singleTypeSchema.xsd"
        f = open(testOutputFile, "w+")
        f.write(renderResult)
        f.close()

    def testSingleTypeSchema2(self):
        modelFile = 'tests/resources/models/json/examples/single_type_schema2.json'
        modelFileExists = os.path.isfile(modelFile)
        self.assertTrue('model file exists: ' + modelFile, modelFileExists)
        model = config.Model()
        model.schema = modelFile
        modelTypes = getModelFromJson(model, [])
        templateFile = 'yacg/generators/templates/xsd.mako'
        template = Template(filename=templateFile)
        templateFileExists = os.path.isfile(modelFile)
        self.assertTrue('template file exists: ' + templateFile, templateFileExists)
        renderResult = template.render(modelTypes=modelTypes, templateParameters={})
        self.assertIsNotNone(renderResult)

        testOutputFile = "tmp/singleTypeSchema2.xsd"
        f = open(testOutputFile, "w+")
        f.write(renderResult)
        f.close()

    def testConfigSchema(self):
        modelFile = 'resources/models/json/yacg_config_schema.json'
        modelFileExists = os.path.isfile(modelFile)
        self.assertTrue('model file exists: ' + modelFile, modelFileExists)
        model = config.Model()
        model.schema = modelFile
        modelTypes = getModelFromJson(model, [])
        templateFile = 'yacg/generators/templates/xsd.mako'
        template = Template(filename=templateFile)
        templateFileExists = os.path.isfile(modelFile)
        self.assertTrue('template file exists: ' + templateFile, templateFileExists)
        renderResult = template.render(modelTypes=modelTypes, templateParameters={})
        self.assertIsNotNone(renderResult)

        testOutputFile = "tmp/yacg_config_schema.xsd"
        f = open(testOutputFile, "w+")
        f.write(renderResult)
        f.close()

    def testCircularTypeDeps(self):
        modelFile = 'tests/resources/models/json/examples/schema_with_circular_deps.json'
        modelFileExists = os.path.isfile(modelFile)
        self.assertTrue('model file exists: ' + modelFile, modelFileExists)
        model = config.Model()
        model.schema = modelFile
        modelTypes = getModelFromJson(model, [])
        templateFile = 'yacg/generators/templates/xsd.mako'
        template = Template(filename=templateFile)
        templateFileExists = os.path.isfile(modelFile)
        self.assertTrue('template file exists: ' + templateFile, templateFileExists)
        renderResult = template.render(modelTypes=modelTypes, templateParameters={})
        self.assertIsNotNone(renderResult)

        testOutputFile = "tmp/schema_with_circular_deps.xsd"
        f = open(testOutputFile, "w+")
        f.write(renderResult)
        f.close()
