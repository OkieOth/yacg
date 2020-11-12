import unittest
from pathlib import Path
import shutil
import os

from yacg.model.config import SingleFileTask, Model
from yacg.builder.jsonBuilder import getModelFromJson
from yacg.generators.singleFileGenerator import renderSingleFileTemplate


class TestProtobuf (unittest.TestCase):
    def testJavaBeanTemplate(self):
        dirpath = Path('tmp', 'javaBeans')
        if dirpath.exists() and dirpath.is_dir():
            shutil.rmtree(dirpath)
        modelFile = 'resources/models/json/yacg_model_schema.json'
        modelFileExists = os.path.isfile(modelFile)
        self.assertTrue('model file exists: ' + modelFile, modelFileExists)
        model = Model()
        model.schema = modelFile
        modelTypes = getModelFromJson(model, [])
        templateFile = 'yacg/generators/templates/protobuf.mako'
        templateFileExists = os.path.isfile(templateFile)
        self.assertTrue('template file exists: ' + templateFile, templateFileExists)
        templateParameters = []
        singleFileTask = SingleFileTask()
        singleFileTask.template = templateFile
        singleFileTask.destFile = 'tmp/yacg.proto'
        singleFileTask.templateParams = templateParameters

        renderSingleFileTemplate(
            modelTypes,
            (),
            (),
            singleFileTask)
