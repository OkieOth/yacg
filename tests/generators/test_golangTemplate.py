import unittest
from pathlib import Path
import shutil
import os

import yacg.generators.helper.generatorHelperFuncs as generatorHelper


from yacg.builder.yamlBuilder import getModelFromYaml
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
        templateParam.value = 'golang.test'
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

