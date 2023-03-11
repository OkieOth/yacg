import unittest
import os.path
from mako.template import Template
from yacg.builder.jsonBuilder import getModelFromJson
from pathlib import Path
import shutil

import yacg.model.config as config
from yacg.model.config import MultiFileTask
from yacg.generators.multiFileGenerator import renderMultiFileTemplate


class TestPlantUml (unittest.TestCase):
    def testSingleTypeSchema(self):
        modelFile = 'tests/resources/models/json/examples/roller.json'
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

        testOutputFile = "tmp/roller.puml"
        f = open(testOutputFile, "w+")
        f.write(renderResult)
        f.close()

    def testJavaBeanTemplate(self):
        dirpath = Path('tmp', 'roller')
        if dirpath.exists() and dirpath.is_dir():
            shutil.rmtree(dirpath)
        modelFile = 'tests/resources/models/json/examples/roller.json'
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
        templateParam.value = 'sharing_platform'
        templateParam2 = config.TemplateParam()
        templateParam2.name = 'noInfo'
        templateParam2.value = 'no'
        templateParameters.append(templateParam)
        templateParameters.append(templateParam2)
        multiFileTask = MultiFileTask()
        multiFileTask.template = templateFile
        multiFileTask.destDir = 'tmp/roller/sharing_platform'
        multiFileTask.destFileExt = 'java'
        multiFileTask.templateParams = templateParameters
        renderMultiFileTemplate(
            modelTypes,
            (),
            (),
            multiFileTask)
