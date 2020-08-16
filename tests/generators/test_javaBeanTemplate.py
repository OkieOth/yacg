import unittest
from pathlib import Path
import shutil
import os

from yacg.builder.jsonBuilder import getModelFromJson
from yacg.generators.multiFileGenerator import renderMultiFileTemplate
from yacg.builder.jsonBuilder import getModelFromJson


import yacg.model.config as config


class TestJavaBean (unittest.TestCase):
    def testJavaBeanTemplate(self):
        dirpath = Path('tmp', 'javaBeans')
        if dirpath.exists() and dirpath.is_dir():
            shutil.rmtree(dirpath)
        modelFile = 'resources/models/json/yacg_model_schema.json'
        modelFileExists = os.path.isfile(modelFile)
        self.assertTrue('model file exists: ' + modelFile, modelFileExists)
        model = config.Model()
        model.schema = modelFile
        modelTypes = getModelFromJson(model, [])
        templateFile = 'resources/templates/examples/javaBeans.mako'
        templateFileExists = os.path.isfile(templateFile)
        self.assertTrue('template file exists: ' + templateFile, templateFileExists)
        templateParameters = []
        templateParam = config.TemplateParam()
        templateParam.name = 'modelPackage'
        templateParam.value = 'de.test.model'
        templateParameters.append(templateParam)
        renderMultiFileTemplate(
            modelTypes,
            templateFile,
            'tmp/javaBeans/de/test/model',
            None,
            None,
            'java',
            templateParameters,
            (),
            ())
