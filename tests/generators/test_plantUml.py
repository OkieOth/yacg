import unittest
import os.path
from mako.template import Template
from yacg.builder.jsonBuilder import getModelFromJson
from yacg.model.config import SingleFileTask

from yacg.generators.singleFileGenerator import renderSingleFileTemplate
import yacg.model.config as config


class TestPlantUml (unittest.TestCase):
    def testSingleTypeSchema(self):
        modelFile = 'tests/resources/models/json/examples/single_type_schema.json'
        modelFileExists = os.path.isfile(modelFile)
        self.assertTrue('model file exists: ' + modelFile, modelFileExists)
        model = config.Model()
        model.schema = modelFile
        modelTypes = getModelFromJson(model, [])
        templateFile = 'yacg/generators/templates/plantUml.mako'
        template = Template(filename=templateFile)
        templateFileExists = os.path.isfile(modelFile)
        self.assertTrue('template file exists: ' + templateFile, templateFileExists)
        renderResult = template.render(modelTypes=modelTypes, templateParameters={})
        self.assertIsNotNone(renderResult)

        testOutputFile = "tmp/singleTypeSchema.puml"
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
        templateFile = 'yacg/generators/templates/plantUml.mako'
        template = Template(filename=templateFile)
        templateFileExists = os.path.isfile(modelFile)
        self.assertTrue('template file exists: ' + templateFile, templateFileExists)
        renderResult = template.render(modelTypes=modelTypes, templateParameters={})
        self.assertIsNotNone(renderResult)

        testOutputFile = "tmp/singleTypeSchema2.puml"
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
        templateFile = 'yacg/generators/templates/plantUml.mako'
        template = Template(filename=templateFile)
        templateFileExists = os.path.isfile(modelFile)
        self.assertTrue('template file exists: ' + templateFile, templateFileExists)
        renderResult = template.render(modelTypes=modelTypes, templateParameters={})
        self.assertIsNotNone(renderResult)

        testOutputFile = "tmp/yacg_config_schema.puml"
        f = open(testOutputFile, "w+")
        f.write(renderResult)
        f.close()

    def testNibelDings(self):
        modelFile = 'tests/resources/models/json/examples/nibelheim.json'
        modelFileExists = os.path.isfile(modelFile)
        self.assertTrue('model file exists: ' + modelFile, modelFileExists)
        model = config.Model()
        model.schema = modelFile
        modelTypes = getModelFromJson(model, [])

        templateFile = 'yacg/generators/templates/plantUml.mako'
        template = Template(filename=templateFile)
        templateFileExists = os.path.isfile(modelFile)
        self.assertTrue('template file exists: ' + templateFile, templateFileExists)
        renderResult = template.render(modelTypes=modelTypes, templateParameters={})
        self.assertIsNotNone(renderResult)

        testOutputFile = "tmp/nibelheim.puml"
        f = open(testOutputFile, "w+")
        f.write(renderResult)
        f.close()

    def _renderPuml(self, modelFile, testOutputFile):
        modelFileExists = os.path.isfile(modelFile)
        self.assertTrue('model file exists: ' + modelFile, modelFileExists)
        model = config.Model()
        model.schema = modelFile
        modelTypes = getModelFromJson(model, [])
        templateFile = 'yacg/generators/templates/plantUml.mako'
        template = Template(filename=templateFile)
        templateFileExists = os.path.isfile(modelFile)
        self.assertTrue('template file exists: ' + templateFile, templateFileExists)
        renderResult = template.render(modelTypes=modelTypes, templateParameters={})
        self.assertIsNotNone(renderResult)

        f = open(testOutputFile, "w+")
        f.write(renderResult)
        f.close()

    def testCircularTypeDeps(self):
        modelFile = 'tests/resources/models/json/examples/schema_with_circular_deps.json'
        testOutputFile = "tmp/schema_with_circular_deps.puml"
        self._renderPuml(modelFile, testOutputFile)

    def testStackedDicts(self):
        modelFile = 'tests/resources/models/json/examples/stacked_dicts.json'
        #self._renderPuml(modelFile, testOutputFile)
        modelFileExists = os.path.isfile(modelFile)
        self.assertTrue('model file exists: ' + modelFile, modelFileExists)
        model = config.Model()
        model.schema = modelFile
        modelTypes = getModelFromJson(model, [])
        templateFile = 'yacg/generators/templates/plantUml.mako'
        singleFileTask = SingleFileTask()
        singleFileTask.template = templateFile
        singleFileTask.destFile = 'tmp/stacked_dicts_v2.puml'

        renderSingleFileTemplate(
            modelTypes,
            (),
            (),
            singleFileTask)
