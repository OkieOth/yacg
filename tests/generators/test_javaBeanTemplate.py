import unittest
from pathlib import Path
import shutil
import os

import yacg.generators.helper.generatorHelperFuncs as generatorHelper


from yacg.builder.jsonBuilder import getModelFromJson
from yacg.builder.yamlBuilder import getModelFromYaml
from yacg.generators.multiFileGenerator import renderMultiFileTemplate
from yacg.model.config import MultiFileTask, MultiFileTaskFileFilterTypeEnum, BlackWhiteListEntry, BlackWhiteListEntryTypeEnum


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
        multiFileTask = MultiFileTask()
        multiFileTask.template = templateFile
        multiFileTask.destDir = 'tmp/javaBeans/de/test/model'
        multiFileTask.destFileExt = 'java'
        multiFileTask.templateParams = templateParameters

        renderMultiFileTemplate(
            modelTypes,
            (),
            (),
            multiFileTask)

    def testBackListedPathTypes(self):
        modelFile = 'resources/models/yaml/userConfig.swagger.yaml'
        model = config.Model()
        model.schema = modelFile
        modelTypes = getModelFromYaml(model, [])
        blackList = []
        blackListEntry = BlackWhiteListEntry()
        blackListEntry.name = 'PathType'
        blackListEntry.type = BlackWhiteListEntryTypeEnum.TYPETYPE
        blackList.append(blackListEntry)
        modelTypesToUse = generatorHelper.trimModelTypes(modelTypes, blackList, ())
        self.assertEqual(18, len(modelTypesToUse))

    def testWhiteListedPathTypes(self):
        modelFile = 'resources/models/yaml/userConfig.swagger.yaml'
        modelFileExists = os.path.isfile(modelFile)
        self.assertTrue('model file exists: ' + modelFile, modelFileExists)
        model = config.Model()
        model.schema = modelFile
        modelTypes = getModelFromYaml(model, [])
        whiteList = []
        whiteListEntry = BlackWhiteListEntry()
        whiteListEntry.name = 'PathType'
        whiteListEntry.type = BlackWhiteListEntryTypeEnum.TYPETYPE
        whiteList.append(whiteListEntry)
        modelTypesToUse = generatorHelper.trimModelTypes(modelTypes, (), whiteList)
        self.assertEqual(2, len(modelTypesToUse))

    def testJavaBeanTemplateWithFilter(self):
        dirpath = Path('tmp', 'javaBeans3')
        if dirpath.exists() and dirpath.is_dir():
            shutil.rmtree(dirpath)
        modelFile = 'resources/models/yaml/userConfig.swagger.yaml'
        modelFileExists = os.path.isfile(modelFile)
        self.assertTrue('model file exists: ' + modelFile, modelFileExists)
        model = config.Model()
        model.schema = modelFile
        modelTypes = getModelFromYaml(model, [])
        templateFile = 'resources/templates/examples/javaBeans.mako'
        templateFileExists = os.path.isfile(templateFile)
        self.assertTrue('template file exists: ' + templateFile, templateFileExists)
        templateParameters = []
        templateParam = config.TemplateParam()
        templateParam.name = 'modelPackage'
        templateParam.value = 'de.test.model'
        templateParameters.append(templateParam)
        multiFileTask = MultiFileTask()
        multiFileTask.template = templateFile
        multiFileTask.destDir = 'tmp/javaBeans3/de/test/model'
        multiFileTask.destFileExt = 'java'
        multiFileTask.upperCaseStartedDestFileName = True
        multiFileTask.templateParams = templateParameters
        blackList = []
        blackListEntry = BlackWhiteListEntry()
        blackListEntry.name = 'PathType'
        blackListEntry.type = BlackWhiteListEntryTypeEnum.TYPETYPE
        blackList.append(blackListEntry)

        renderMultiFileTemplate(
            modelTypes,
            blackList,
            (),
            multiFileTask)
