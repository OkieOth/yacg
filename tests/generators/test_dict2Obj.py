import unittest
import os.path
from mako.template import Template
from yacg.builder.jsonBuilder import getModelFromJson

import yacg.model.config as config
import yacg.generators.helper.generatorHelperFuncs as generatorHelperFuncs


class TestDictToObject (unittest.TestCase):
    def testConfigSchema(self):
        modelFile = 'resources/models/json/yacg_config_schema.json'
        modelFileExists = os.path.isfile(modelFile)
        self.assertTrue('model file exists: ' + modelFile, modelFileExists)
        model = config.Model()
        model.schema = modelFile
        modelTypes = getModelFromJson(model, [])
        templateFile = 'resources/templates/examples/pythonBeans.mako'
        template = Template(filename=templateFile)
        templateFileExists = os.path.isfile(modelFile)
        self.assertTrue('template file exists: ' + templateFile, templateFileExists)
        templateParameterDict = {}
        templateParameterDict['baseModelDomain'] = 'yacg.model.config'
        renderResult = template.render(modelTypes=modelTypes, templateParameters=templateParameterDict)
        self.assertIsNotNone(renderResult)

        testOutputFile = "tmp/config.py"
        f = open(testOutputFile, "w+")
        f.write(renderResult)
        f.close()

    def testModelSchema(self):
        modelFile = 'resources/models/json/yacg_model_schema.json'
        modelFileExists = os.path.isfile(modelFile)
        self.assertTrue('model file exists: ' + modelFile, modelFileExists)
        model = config.Model()
        model.schema = modelFile
        modelTypes = getModelFromJson(model, [])
        templateFile = 'resources/templates/examples/pythonBeans.mako'
        template = Template(filename=templateFile)
        templateFileExists = os.path.isfile(modelFile)
        self.assertTrue('template file exists: ' + templateFile, templateFileExists)
        templateParameterDict = {}
        templateParameterDict['baseModelDomain'] = 'yacg.model.model'
        renderResult = template.render(modelTypes=modelTypes, templateParameters=templateParameterDict)
        self.assertIsNotNone(renderResult)

        testOutputFile = "tmp/model.py"
        f = open(testOutputFile, "w+")
        f.write(renderResult)
        f.close()

    def testEvilSchema(self):
        modelFile = 'tests/resources/models/json/examples/evil_enum.json'
        modelFileExists = os.path.isfile(modelFile)
        self.assertTrue('model file exists: ' + modelFile, modelFileExists)
        model = config.Model()
        model.schema = modelFile
        modelTypes = getModelFromJson(model, [])
        templateFile = 'resources/templates/examples/pythonBeans.mako'
        template = Template(filename=templateFile)
        templateFileExists = os.path.isfile(modelFile)
        self.assertTrue('template file exists: ' + templateFile, templateFileExists)
        templateParameterDict = {}
        templateParameterDict['baseModelDomain'] = 'yacg.model.model'
        renderResult = template.render(modelTypes=modelTypes, templateParameters=templateParameterDict)
        self.assertIsNotNone(renderResult)

        testOutputFile = "tmp/evil_model.py"
        f = open(testOutputFile, "w+")
        f.write(renderResult)
        f.close()

    def testEvilSchema2(self):
        modelFile = 'tests/resources/models/json/examples/evil_enum.json'
        modelFileExists = os.path.isfile(modelFile)
        self.assertTrue('model file exists: ' + modelFile, modelFileExists)
        model = config.Model()
        model.schema = modelFile
        modelTypes = getModelFromJson(model, [])
        templateFile = 'resources/templates/examples/pythonBeansTests.mako'
        template = Template(filename=templateFile)
        templateFileExists = os.path.isfile(modelFile)
        self.assertTrue('template file exists: ' + templateFile, templateFileExists)
        templateParameterDict = {}
        templateParameterDict['baseModelDomain'] = 'yacg.model.model'
        renderResult = template.render(modelTypes=modelTypes, templateParameters=templateParameterDict)
        self.assertIsNotNone(renderResult)

        testOutputFile = "tmp/evil_model_tests.py"
        f = open(testOutputFile, "w+")
        f.write(renderResult)
        f.close()

    def testOpenApiSchema(self):
        modelFile = 'resources/models/json/yacg_openapi_paths.json'
        modelFileExists = os.path.isfile(modelFile)
        self.assertTrue('model file exists: ' + modelFile, modelFileExists)
        model = config.Model()
        model.schema = modelFile
        modelTypes = getModelFromJson(model, [])
        templateFile = 'resources/templates/examples/pythonBeans.mako'
        template = Template(filename=templateFile)
        templateFileExists = os.path.isfile(modelFile)
        self.assertTrue('template file exists: ' + templateFile, templateFileExists)
        templateParameterDict = {}
        templateParameterDict['baseModelDomain'] = 'yacg.model.openapi'

        blackListList = []
        # all types from the main model should be igrnored ...
        # blacklisted by domain example
        entryTag = config.BlackWhiteListEntry()
        entryTag.name = 'yacgCore'
        entryTag.type = config.BlackWhiteListEntryTypeEnum.DOMAIN
        blackListList.append(entryTag)
        trimmedTypes = generatorHelperFuncs.trimModelTypes(modelTypes, blackListList, None)

        renderResult = template.render(
            modelTypes=trimmedTypes,
            templateParameters=templateParameterDict)
        self.assertIsNotNone(renderResult)

        testOutputFile = "tmp/openapi.py"
        f = open(testOutputFile, "w+")
        f.write(renderResult)
        f.close()

    def testModelSchemaTests(self):
        modelFile = 'resources/models/json/yacg_model_schema.json'
        modelFileExists = os.path.isfile(modelFile)
        self.assertTrue('model file exists: ' + modelFile, modelFileExists)
        model = config.Model()
        model.schema = modelFile
        modelTypes = getModelFromJson(model, [])

        templateFile = 'resources/templates/examples/pythonBeansTests.mako'
        template = Template(filename=templateFile)
        templateFileExists = os.path.isfile(modelFile)
        self.assertTrue('template file exists: ' + templateFile, templateFileExists)
        templateParameterDict = {}
        templateParameterDict['modelPackage'] = 'yacg.model.model'
        renderResult = template.render(
            modelTypes=modelTypes,
            templateParameters=templateParameterDict)
        self.assertIsNotNone(renderResult)

        testOutputFile = "tmp/test_model.py"
        f = open(testOutputFile, "w+")
        f.write(renderResult)
        f.close()
