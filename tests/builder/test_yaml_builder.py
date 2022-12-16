import unittest
import os.path
from yacg.builder.yamlBuilder import getModelFromYaml
from yacg.model.model import EnumType, Type
import yacg.model.randomFuncs as randomFuncs
import yacg.model.config as config


class TestYamlBuilder (unittest.TestCase):
    def testSingleTypeSchema(self):
        modelFile = 'resources/models/yaml/yacg_config_schema.yaml'
        modelFileExists = os.path.isfile(modelFile)
        self.assertTrue('model file exists: ' + modelFile, modelFileExists)
        model = config.Model()
        model.schema = modelFile
        modelTypes = getModelFromYaml(model, [])
        self.assertIsNotNone(modelTypes)
        self.assertEqual(8, len(modelTypes))

        self._checkUpType(0, 'Job', 4, modelTypes)
        self._checkUpType(1, 'Model', 4, modelTypes)
        self._checkUpType(2, 'Task', 6, modelTypes)
        self._checkUpType(3, 'BlackWhiteListEntry', 2, modelTypes)
        self._checkUpType(4, 'BlackWhiteListEntryTypeEnum', 0, modelTypes)
        self._checkUpType(5, 'SingleFileTask', 3, modelTypes)
        self._checkUpType(6, 'TemplateParam', 2, modelTypes)
        self._checkUpType(7, 'MultiFileTask', 6, modelTypes)

    def _checkUpType(self, position, typeName, propCount, modelTypes):
        type = modelTypes[position]
        self.assertIsNotNone(type)
        self.assertEqual(typeName, type.name)
        if isinstance(type, EnumType) or isinstance(type, Type):
            return type
        self.assertEqual(propCount, len(type.properties))
        for prop in type.properties:
            self.assertIsNotNone(prop.type, "property w/o a type: %s.%s" % (typeName, prop.name))
            if prop.name.endswith('s') or prop.name.endswith('ed'):
                self.assertTrue(prop.isArray, "property has to be an array: %s.%s" % (typeName, prop.name))
            else:
                self.assertFalse(prop.isArray, "property should be no array: %s.%s" % (typeName, prop.name))

    def testXProcessing(self):
        modelFile = 'tests/resources/models/yaml/examples/layer_annotated.yaml'
        modelFileExists = os.path.isfile(modelFile)
        self.assertTrue('model file exists: ' + modelFile, modelFileExists)
        model = config.Model()
        model.schema = modelFile
        modelTypes = getModelFromYaml(model, [])
        self.assertIsNotNone(modelTypes)
        self.assertEqual(12, len(modelTypes))
        found = 0
        for m in modelTypes:
            if m.name == "Layer":
                found = found + 1
                self.assertIsNotNone(m.processing)
                for p in m.properties:
                    self.assertIsNone(p.processing)
            elif m.name == "Geometry":
                found = found + 1
                self.assertIsNotNone(m.processing)
            elif m.name == "DisplayConfigFill":
                self.assertIsNotNone(m.properties[0].processing)
                self.assertEqual(len(m.properties), 1)
            elif m.processing is not None:
                found = found + 1
        self.assertEqual(found, 2)
        randomFuncs.extendMetaModelWithRandomConfigTypes(modelTypes)
        found = 0
        for m in modelTypes:
            if m.name == "Layer":
                found = found + 1
                self.assertIsNotNone(m.processing)
                for p in m.properties:
                    self.assertIsNone(p.processing)
            elif m.name == "Geometry":
                found = found + 1
                self.assertIsNotNone(m.processing)
            elif m.name == "DisplayConfigFill":
                self.assertIsNotNone(m.properties[0].processing)
                self.assertEqual(len(m.properties), 1)
            elif m.processing is not None:
                found = found + 1
        self.assertEqual(found, 2)

if __name__ == '__main__':
    unittest.main()
