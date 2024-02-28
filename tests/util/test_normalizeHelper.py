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

    def test_t1(self):
        dirpath = Path('tmp', 'normalized')
        if dirpath.exists() and dirpath.is_dir():
            shutil.rmtree(dirpath)
        os.mkdir(dirpath)
        modelFile = 'tests/resources/models/yaml/examples/asyncapi_t.yaml'
        schemaAsDict = builder.getParsedSchemaFromYaml(modelFile)
        extractedTypes = builder.extractTypes(schemaAsDict, modelFile, [], False)
        localTypePrefix = modelFuncs.getLocalTypePrefix(schemaAsDict)

        normalizeHelper.normalizeSchema(schemaAsDict, extractedTypes, modelFile, 'tmp/normalized/asyncapi_t.json', localTypePrefix)
        normalizeHelper.normalizeSchema(schemaAsDict, extractedTypes, modelFile, 'tmp/normalized/asyncapi_t.yaml', localTypePrefix)

    def test_t2(self):
        dirpath = Path('tmp', 'normalized')
        if dirpath.exists() and dirpath.is_dir():
            shutil.rmtree(dirpath)
        os.mkdir(dirpath)
        modelFile = 'tests/resources/models/json/examples/asyncapi_s.json'
        schemaAsDict = builder.getParsedSchemaFromYaml(modelFile)
        extractedTypes = builder.extractTypes(schemaAsDict, modelFile, [], False)
        localTypePrefix = modelFuncs.getLocalTypePrefix(schemaAsDict)

        normalizeHelper.normalizeSchema(schemaAsDict, extractedTypes, modelFile, 'tmp/normalized/asyncapi_t.json', localTypePrefix)
        componentsDict = schemaAsDict.get("components", None)
        self.assertIsNotNone(componentsDict)
        schemasDict = componentsDict.get("schemas", None)
        self.assertIsNotNone(schemasDict)
        tttDict = schemasDict.get("TTT", None)
        self.assertIsNotNone(tttDict)
        propertiesDict = tttDict.get("properties", None)
        self.assertIsNotNone(propertiesDict)
        guidDict = propertiesDict.get("guid", None)
        self.assertIsNotNone(guidDict)
        description = guidDict.get("description", None)
        self.assertIsNotNone(description)
        nameDict = propertiesDict.get("name", None)
        self.assertIsNotNone(nameDict)
        description = propertiesDict.get("description", None)
        self.assertIsNone(description)

        tttNodeDict = schemasDict.get("TTTNode", None)
        self.assertIsNotNone(tttNodeDict)
        allOfArray = tttNodeDict.get("allOf", None)
        self.assertIsNotNone(allOfArray)
        propertiesDict = allOfArray[1].get("properties", None)
        self.assertIsNotNone(propertiesDict)
        yyyDict = propertiesDict.get("yyy", None)
        self.assertIsNotNone(yyyDict)
        self.assertIsNone(yyyDict.get('items', None))
        self.assertEqual(yyyDict.get("type", ""), "string")
        self.assertEqual(yyyDict.get("format", ""), "uuid")
        subNodesDict = propertiesDict.get("subNodes", None)
        self.assertIsNotNone(subNodesDict)
        self.assertIsNone(subNodesDict.get('description', None))
        self.assertIsNone(description)
        self.assertIsNotNone(subNodesDict.get('items', None))
        self.assertEqual(subNodesDict.get("type", ""), "array")
        detectorsDict = propertiesDict.get("detectors", None)
        self.assertIsNotNone(detectorsDict)
        self.assertIsNotNone(detectorsDict.get('description', None))
        self.assertIsNotNone(detectorsDict.get('items', None))
        self.assertEqual(detectorsDict.get("type", ""), "array")
        dddDict = schemasDict.get("DDD", None)
        self.assertIsNotNone(dddDict)
        dddAllOfArray = dddDict.get("allOf", None)
        self.assertIsNotNone(dddAllOfArray)
