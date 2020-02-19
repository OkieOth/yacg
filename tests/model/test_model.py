import unittest
import yacg
from yacg.model.model import Type, BaseType 
from yacg.model.model import IntegerType, NumberType
from yacg.model.model import StringType
from yacg.model.model import DateType, DateTimeType
from yacg.model.model import EnumType, ComplexType
from yacg.model.model import Property, Tag


class TestModelClasses (unittest.TestCase):
    def testType(self):
        x = Type('test')
        self.assertIsNotNone (x)
        self.assertEqual('test',x.name)        

    def testBaseType(self):        
        pass

    def testIntegerType(self):        
        pass

    def testNumberType(self):        
        pass

    def testStringType(self):        
        pass

    def testDateType(self):        
        pass

    def testDateTimeType(self):        
        pass

    def testEnumType(self):        
        pass

    def testComplexType(self):        
        pass

    def testProperty(self):        
        pass

    def testTag(self):        
        pass

if __name__ == '__main__':
    unittest.main()