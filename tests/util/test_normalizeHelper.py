import unittest
from pathlib import Path
import shutil
import os
import yacg.util.normalize_helper as normalizeHelper
import yacg.builder.impl.dictionaryBuilder as builder
import yacg.model.modelFuncs as modelFuncs


class TestNormalizeHelper (unittest.TestCase):
    def testNormalizeSchema(self):
        dirpath = Path('tmp', 'normalized')
        if dirpath.exists() and dirpath.is_dir():
            shutil.rmtree(dirpath)
        os.mkdir(dirpath)
        modelFile = 'resources/models/json/yacg_asyncapi_types.json'
        schemaAsDict = builder.getParsedSchemaFromJson(modelFile)
        extractedTypes = builder.extractTypes(schemaAsDict, modelFile, [], False)
        localTypePrefix = modelFuncs.getLocalTypePrefix(schemaAsDict)

        normalizeHelper.normalizeSchema(schemaAsDict, extractedTypes, modelFile, 'tmp/normalized/yacg_asyncapi_types.json', localTypePrefix)
        normalizeHelper.normalizeSchema(schemaAsDict, extractedTypes, modelFile, 'tmp/normalized/yacg_asyncapi_types.yaml', localTypePrefix)

    def testNormalizeOpenApi(self):
        dirpath = Path('tmp', 'normalized')
        if dirpath.exists() and dirpath.is_dir():
            shutil.rmtree(dirpath)
        os.mkdir(dirpath)
        modelFile = 'tests/resources/models/yaml/examples/openapi_layer.yaml'
        schemaAsDict = builder.getParsedSchemaFromYaml(modelFile)
        extractedTypes = builder.extractTypes(schemaAsDict, modelFile, [], False)
        localTypePrefix = modelFuncs.getLocalTypePrefix(schemaAsDict)
        normalizeHelper._normalizeImpl(schemaAsDict, extractedTypes, modelFile, localTypePrefix)
        componentsDict = schemaAsDict.get("components", None)
        self.assertIsNotNone(componentsDict)
        schemasDict = componentsDict.get("schemas", None)
        self.assertIsNotNone(schemasDict)
        lineStringDict = schemasDict.get("LineString", None)
        self.assertIsNotNone(lineStringDict)
        propertiesDict = lineStringDict.get("properties", None)
        self.assertIsNotNone(propertiesDict)
        self.assertEqual(len(propertiesDict["type"]["enum"]), 1)
        self.assertEqual(propertiesDict["type"]["enum"][0], "LineString")
