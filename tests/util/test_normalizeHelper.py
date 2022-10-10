import unittest
from pathlib import Path
import shutil
import os
import yacg.util.normalize_helper as normalizeHelper
import yacg.builder.impl.dictionaryBuilder as builder


class TestNormalizeHelper (unittest.TestCase):
    def testNormalizeSchema(self):
        dirpath = Path('tmp', 'normalized')
        if dirpath.exists() and dirpath.is_dir():
            shutil.rmtree(dirpath)
        os.mkdir(dirpath)
        modelFile = 'resources/models/json/yacg_asyncapi_types.json'
        schemaAsDict = builder.getParsedSchemaFromJson(modelFile)
        extractedTypes = builder.extractTypes(schemaAsDict, modelFile, [], False)
        normalizeHelper.normalizeSchema(schemaAsDict, extractedTypes, modelFile, 'tmp/normalized/yacg_asyncapi_types.json')
        normalizeHelper.normalizeSchema(schemaAsDict, extractedTypes, modelFile, 'tmp/normalized/yacg_asyncapi_types.yaml')

    def testNormalizeSchema2(self):
        dirpath = Path('tmp', 'normalized')
        if dirpath.exists() and dirpath.is_dir():
            shutil.rmtree(dirpath)
        os.mkdir(dirpath)
        modelFile = '/home/eikothomas/prog/git.swarco.com/cip/swarco.core.service.device-state-manager/api/asyncapi/dsm.yaml'
        schemaAsDict = builder.getParsedSchemaFromYaml(modelFile)
        extractedTypes = builder.extractTypes(schemaAsDict, modelFile, [], False)
        normalizeHelper.normalizeSchema(schemaAsDict, extractedTypes, modelFile, 'tmp/normalized/dsm.yaml')
