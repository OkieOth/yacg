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
        extractedTypes = builder.extractTypes(schemaAsDict, modelFile, [], True)
        normalizeHelper.normalizeSchema(schemaAsDict, extractedTypes, modelFile, 'tmp/normalized/yacg_asyncapi_types.json')
        normalizeHelper.normalizeSchema(schemaAsDict, extractedTypes, modelFile, 'tmp/normalized/yacg_asyncapi_types.yaml')
