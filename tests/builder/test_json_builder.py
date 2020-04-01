import unittest
import os.path
from yacg.builder.jsonBuilder import getModelFromJson
from yacg.model.model import IntegerType, NumberType
from yacg.model.model import StringType, UuidType
from yacg.model.model import DateType, DateTimeType
from yacg.model.model import EnumType, ComplexType


class TestJsonBuilder (unittest.TestCase):
    def testSingleTypeSchema(self):
        modelFile = 'resources/models/json/examples/single_type_schema.json'
        modelFileExists = os.path.isfile(modelFile)
        self.assertTrue ('model file exists: '+ modelFile,modelFileExists)
        modelTypes = getModelFromJson (modelFile)
        self.assertIsNotNone (modelTypes)
        self.assertEqual(3,len(modelTypes))

        mainType = None
        anotherType = None
        innerComplexType = None
        for type in modelTypes:
            if type.name == 'SingleTypeSchema':
                mainType = type
            elif type.name == 'AnotherType':
                anotherType = type
            else:
                innerComplexType = type
        self.assertIsNotNone (mainType)
        self.assertEqual(4,len(mainType.properties))
        self.assertTrue (isinstance (mainType.properties[0].type, StringType)) 
        self.assertTrue (isinstance (mainType.properties[1].type, NumberType)) 
        self.assertTrue (isinstance (mainType.properties[2].type, EnumType)) 
        self.assertTrue (isinstance (mainType.properties[3].type, ComplexType)) 

        self.assertIsNotNone (anotherType)
        self.assertEqual(2,len(anotherType.properties))
        self.assertTrue (isinstance (anotherType.properties[0].type, DateTimeType)) 
        self.assertTrue (isinstance (anotherType.properties[1].type, NumberType)) 

        self.assertIsNotNone (innerComplexType)
        self.assertEqual(3,len(innerComplexType.properties))
        self.assertTrue (isinstance (innerComplexType.properties[0].type, StringType)) 
        self.assertTrue (isinstance (innerComplexType.properties[1].type, IntegerType)) 
        self.assertTrue (isinstance (innerComplexType.properties[2].type, ComplexType)) 
        self.assertEqual(anotherType, innerComplexType.properties[2].type)

    def testSingleTypeSchema(self):
        modelFile = 'resources/models/json/config_schema.json'
        modelFileExists = os.path.isfile(modelFile)
        self.assertTrue ('model file exists: '+ modelFile,modelFileExists)
        modelTypes = getModelFromJson (modelFile)
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

    def testSchemaWithExternalRef(self):
        modelFile = 'resources/models/json/examples/schema_with_external_ref.json'
        modelFileExists = os.path.isfile(modelFile)
        self.assertTrue ('model file exists: '+ modelFile,modelFileExists)
        modelTypes = getModelFromJson (modelFile)
        self.assertIsNotNone (modelTypes)
        self.assertEqual (3,len(modelTypes))
        self._checkUpType(0,'OneType',2,modelTypes)
        self._checkUpType(1,'TwoType',3,modelTypes)
        self._checkUpType(2,'AnotherType',2,modelTypes)

    def testSchemaWithExternalCircularRefs(self):
        modelFile = 'resources/models/json/examples/schema_with_circular_deps.json'
        modelFileExists = os.path.isfile(modelFile)
        self.assertTrue ('model file exists: '+ modelFile,modelFileExists)
        modelTypes = getModelFromJson (modelFile)
        self.assertIsNotNone (modelTypes)
        self.assertEqual(5,len(modelTypes))

        self._checkUpType(0,'OneType',2,modelTypes)
        self._checkUpType(1,'RefBackType',4,modelTypes)
        self._checkUpType(2,'RefBackType2',3,modelTypes)
        self._checkUpType(3,'TwoType',3,modelTypes)
        self._checkUpType(4,'AnotherType',2,modelTypes)

    def testSimpleAllOf(self):
        modelFile = 'resources/models/json/examples/simple_allof.json'
        modelFileExists = os.path.isfile(modelFile)
        self.assertTrue ('model file exists: '+ modelFile,modelFileExists)
        modelTypes = getModelFromJson (modelFile)
        self.assertIsNotNone (modelTypes)
        self.assertEqual(3,len(modelTypes))
        self._checkUpType(0,'SimpleAllOfSchema',1,modelTypes)
        self._checkUpType(1,'Address',3,modelTypes)
        self._checkUpType(2,'SimpleAllOfSchemaTypeEnum',0,modelTypes)

    def testSophisticatedAllOf(self):
        modelFile = 'resources/models/json/examples/more_sophisticated_allof.json'
        modelFileExists = os.path.isfile(modelFile)
        self.assertTrue ('model file exists: '+ modelFile,modelFileExists)
        modelTypes = getModelFromJson (modelFile)
        self.assertIsNotNone (modelTypes)
        self.assertEqual(5,len(modelTypes))
        type = self._checkUpType(0,'MoreSophisticatedAllOf',1,modelTypes)
        self.assertIsNotNone(type.extendsType)
        address = self._checkUpType(1,'Address',3,modelTypes)
        self.assertEqual(type.extendsType,address)
        self._checkUpType(2,'MoreSophisticatedAllOfTypeEnum',0,modelTypes)
        self._checkUpType(3,'MainAddress',2,modelTypes)
        self._checkUpType(4,'MainAddressComplex',3,modelTypes)


    def _checkUpType(self,position,typeName,propCount,modelTypes):
        type = modelTypes[position]
        self.assertIsNotNone(type)
        self.assertIsNotNone(type.source)
        sourceExists = os.path.isfile(type.source)
        self.assertTrue ('source file exists: '+ type.source,sourceExists)
        self.assertEqual(typeName,type.name)
        self.assertEqual(propCount,len(type.properties))
        for prop in type.properties:
            self.assertIsNotNone(prop.type,"property w/o a type: %s.%s" % (typeName,prop.name))
            if prop.name.endswith('s') or prop.name.endswith('ed'):
                self.assertTrue(prop.isArray, "property has to be an array: %s.%s" % (typeName,prop.name))
            else: 
                self.assertFalse(prop.isArray, "property should be no array: %s.%s" % (typeName,prop.name))
        return type



if __name__ == '__main__':
    unittest.main()