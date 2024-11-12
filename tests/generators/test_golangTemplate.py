import unittest
from pathlib import Path
import shutil
import os

import yacg.generators.helper.generatorHelperFuncs as generatorHelper


from yacg.builder.yamlBuilder import getModelFromYaml
from yacg.builder.jsonBuilder import getModelFromJson
from yacg.generators.singleFileGenerator import renderSingleFileTemplate
from yacg.model.config import SingleFileTask


import yacg.model.config as config


class TestGoLang (unittest.TestCase):
    def testGolangTemplate(self):
        dirpath = Path('tmp', 'golang')
        if dirpath.exists() and dirpath.is_dir():
            shutil.rmtree(dirpath)
        modelFile = 'resources/models/yaml/layer.yaml'
        modelFileExists = os.path.isfile(modelFile)
        self.assertTrue('model file exists: ' + modelFile, modelFileExists)
        model = config.Model()
        model.schema = modelFile
        modelTypes = getModelFromYaml(model, [])
        templateFile = 'resources/templates/examples/golang.mako'
        templateFileExists = os.path.isfile(templateFile)
        self.assertTrue('template file exists: ' + templateFile, templateFileExists)
        templateParameters = []
        templateParam = config.TemplateParam()
        templateParam.name = 'modelPackage'
        templateParam.value = 'golang_test'
        templateParameters.append(templateParam)
        singleFileTask = SingleFileTask()
        singleFileTask.template = templateFile
        singleFileTask.destFile = 'tmp/golang/layer.go'
        singleFileTask.templateParams = templateParameters

        renderSingleFileTemplate(
            modelTypes,
            (),
            (),
            singleFileTask)

    def testGolangTemplate(self):
        dirpath = Path('tmp', 'golang3')
        if dirpath.exists() and dirpath.is_dir():
            shutil.rmtree(dirpath)
        modelFile = 'resources/models/yaml/layer.yaml'
        modelFileExists = os.path.isfile(modelFile)
        self.assertTrue('model file exists: ' + modelFile, modelFileExists)
        model = config.Model()
        model.schema = modelFile
        modelTypes = getModelFromYaml(model, [])
        templateFile = 'yacg/generators/templates/golang.mako'
        templateParameters = []
        templateParam = config.TemplateParam()
        templateParam.name = 'modelPackage'
        templateParam.value = 'golang_test'
        templateParameters.append(templateParam)
        singleFileTask = SingleFileTask()
        singleFileTask.template = templateFile
        singleFileTask.destFile = 'tmp/golang3/layer.go'
        singleFileTask.templateParams = templateParameters

        renderSingleFileTemplate(
            modelTypes,
            (),
            (),
            singleFileTask)


    def testEvilEnum(self):
        dirpath = Path('tmp', 'golang2')
        if dirpath.exists() and dirpath.is_dir():
            shutil.rmtree(dirpath)
        modelFile = 'tests/resources/models/json/examples/evil_enum_with_values.json'
        modelFileExists = os.path.isfile(modelFile)
        self.assertTrue('model file exists: ' + modelFile, modelFileExists)
        model = config.Model()
        model.schema = modelFile
        modelTypes = getModelFromJson(model, [])
        templateFile = 'resources/templates/examples/golang.mako'
        templateFileExists = os.path.isfile(templateFile)
        self.assertTrue('template file exists: ' + templateFile, templateFileExists)
        templateParameters = []
        templateParam = config.TemplateParam()
        templateParam.name = 'modelPackage'
        templateParam.value = 'golang_test'
        templateParameters.append(templateParam)
        singleFileTask = SingleFileTask()
        singleFileTask.template = templateFile
        singleFileTask.destFile = 'tmp/golang2/evil_enum.go'
        singleFileTask.templateParams = templateParameters

        renderSingleFileTemplate(
            modelTypes,
            (),
            (),
            singleFileTask)
