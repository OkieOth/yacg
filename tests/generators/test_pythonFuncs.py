import unittest
import yacg.generators.helper.pythonFuncs as pythonFuncs
import yacg.model.model as model


class TestPythonFuncs (unittest.TestCase):
    def testGetPythonValueForTypeStringType(self):
        stringType = model.StringType()
        self.assertEqual(
            'None',
            pythonFuncs.getPythonValueForType(stringType, None))
        self.assertEqual(
            'None',
            pythonFuncs.getPythonValueForType(stringType, 'None'))
        self.assertEqual(
            'None',
            pythonFuncs.getPythonValueForType(stringType, 'None'))
        self.assertEqual(
            '"Test"',
            pythonFuncs.getPythonValueForType(stringType, 'Test'))

    def testGetPythonValueForTypeBooeanType(self):
        booleanType = model.BooleanType()
        self.assertEqual(
            'None',
            pythonFuncs.getPythonValueForType(booleanType, None))
        self.assertEqual(
            'None',
            pythonFuncs.getPythonValueForType(booleanType, 'None'))
        self.assertEqual(
            'True',
            pythonFuncs.getPythonValueForType(booleanType, 'true'))
        self.assertEqual(
            'False',
            pythonFuncs.getPythonValueForType(booleanType, 'false'))
        self.assertEqual(
            'False',
            pythonFuncs.getPythonValueForType(booleanType, 'xxx'))

    def testGetPythonValueForTypeIntegerType(self):
        type = model.IntegerType()
        self.assertEqual(
            'None',
            pythonFuncs.getPythonValueForType(type, None))
        self.assertEqual(
            'None',
            pythonFuncs.getPythonValueForType(type, 'None'))
        self.assertEqual(
            '12',
            pythonFuncs.getPythonValueForType(type, '12'))
        self.assertEqual(
            '12',
            pythonFuncs.getPythonValueForType(type, 12))
        self.assertEqual(
            '0',
            pythonFuncs.getPythonValueForType(type, 0))
        self.assertEqual(
            '0',
            pythonFuncs.getPythonValueForType(type, '0'))

    def testGetPythonValueForTypeNumberType(self):
        type = model.NumberType()
        self.assertEqual(
            'None',
            pythonFuncs.getPythonValueForType(type, None))
        self.assertEqual(
            'None',
            pythonFuncs.getPythonValueForType(type, 'None'))
        self.assertEqual(
            '12.3',
            pythonFuncs.getPythonValueForType(type, '12.3'))
        self.assertEqual(
            '12.3',
            pythonFuncs.getPythonValueForType(type, 12.3))
        self.assertEqual(
            '0',
            pythonFuncs.getPythonValueForType(type, 0))
        self.assertEqual(
            '0',
            pythonFuncs.getPythonValueForType(type, '0'))

    def testGetPythonValueForTypeEnumType(self):
        type = model.EnumType()
        type.name = 'TestEnum'
        self.assertEqual(
            'None',
            pythonFuncs.getPythonValueForType(type, None))
        self.assertEqual(
            'None',
            pythonFuncs.getPythonValueForType(type, 'None'))
        self.assertEqual(
            'TestEnum.TEST',
            pythonFuncs.getPythonValueForType(type, 'test'))
