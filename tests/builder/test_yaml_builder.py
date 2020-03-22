import unittest
import os.path
from yacg.builder.yamlBuilder import getModelFromYaml
from yacg.model.model import IntegerType, NumberType
from yacg.model.model import StringType, UuidType
from yacg.model.model import DateType, DateTimeType
from yacg.model.model import EnumType, ComplexType


class TestYamlBuilder (unittest.TestCase):
    def testSingleTypeSchema(self):
        modelFile = 'resources/models/yaml/config_schema.yaml'
        modelFileExists = os.path.isfile(modelFile)
        self.assertTrue ('model file exists: '+ modelFile,modelFileExists)
        modelTypes = getModelFromYaml (modelFile)
        self.assertIsNotNone (modelTypes)
        self.assertEqual(8,len(modelTypes))

        self._checkUpType(0,'Job',4,modelTypes)
        self._checkUpType(1,'Model',4,modelTypes)
        self._checkUpType(2,'Task',6,modelTypes)
        self._checkUpType(3,'BlackWhiteListEntry',2,modelTypes)
        self._checkUpType(4,'BlackWhiteListEntryTypeEnum',0,modelTypes)
        self._checkUpType(5,'SingleFileTask',3,modelTypes)
        self._checkUpType(6,'TemplateParam',2,modelTypes)
        self._checkUpType(7,'MultiFileTask',6,modelTypes)

    def _checkUpType(self,position,typeName,propCount,modelTypes):
        type = modelTypes[position]
        self.assertIsNotNone(type)
        self.assertEqual(typeName,type.name)
        self.assertEqual(propCount,len(type.properties))
        for prop in type.properties:
            self.assertIsNotNone(prop.type,"property w/o a type: %s.%s" % (typeName,prop.name))
            if prop.name.endswith('s') or prop.name.endswith('ed'):
                self.assertTrue(prop.isArray, "property has to be an array: %s.%s" % (typeName,prop.name))
            else: 
                self.assertFalse(prop.isArray, "property should be no array: %s.%s" % (typeName,prop.name))



if __name__ == '__main__':
    unittest.main()