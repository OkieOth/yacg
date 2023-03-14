import unittest
import yacg.model.randomFuncs as randomFuncs
import yacg.model.random_config as randomConfig
import yacg.model.model as model
import createRandomData


class TestRandomFuncs (unittest.TestCase):
    def test1(self):
        defaultConfig = randomConfig.RamdonDefaultConfig()

        type = model.ComplexType()
        type.name = "Test"
        type.processing = randomConfig.RandomDataTypeConf()
        type.processing.randElemCount = 1
        prop = model.Property()
        prop.name = "myInt"
        prop.type = model.IntegerType()
        prop.required = True
        prop2 = model.Property()
        prop2.name = "myString"
        prop2.type = model.StringType()
        prop2.required = True
        type.properties.append(prop)
        type.properties.append(prop2)

        ret = randomFuncs.generateRandomData(type, defaultConfig)
        self.assertTrue(isinstance(ret, dict))
        self.assertIsNotNone(ret.get("myInt", None))
        self.assertIsNotNone(ret.get("myString", None))
        pass

    def test2(self):
        defaultConfig = randomConfig.RamdonDefaultConfig()

        type = model.ComplexType()
        type.name = "Test"
        type.processing = randomConfig.RandomDataTypeConf()
        type.processing.randElemCount = 10
        prop = model.Property()
        prop.name = "myInt"
        prop.type = model.IntegerType()
        prop2 = model.Property()
        prop2.name = "myString"
        prop2.required = True
        prop2.type = model.StringType()
        type.properties.append(prop)
        type.properties.append(prop2)

        ret = randomFuncs.generateRandomData(type, defaultConfig)
        self.assertTrue(isinstance(ret, list))
        self.assertEqual(len(ret), 10)

        ok = False
        for i in range(10):
            if ret[i].get("myInt", None) is None:
                ok = True
            self.assertIsNotNone(ret[i].get("myString", None))
        self.assertTrue(ok)

    def test3(self):
        defaultConfig = randomConfig.RamdonDefaultConfig()

        type = model.ComplexType()
        type.name = "Test"
        type.processing = randomConfig.RandomDataTypeConf()
        type.processing.randMinElemCount = 2
        type.processing.randMaxElemCount = 9
        prop = model.Property()
        prop.name = "myInt"
        prop.type = model.IntegerType()
        prop2 = model.Property()
        prop2.name = "myString"
        prop2.required = True
        prop2.type = model.StringType()
        type.properties.append(prop)
        type.properties.append(prop2)

        i = 0
        ok = False
        while i < 10:
            ret = randomFuncs.generateRandomData(type, defaultConfig)
            self.assertTrue(isinstance(ret, list))
            lRet = len(ret)
            if (lRet > 2) and (lRet < 9):
                ok = True
                break
            i = i + 1
        self.assertTrue(ok)
        pass

    def testArrayType1(self):
        defaultConfig = randomConfig.RamdonDefaultConfig()

        type = model.ArrayType()
        type.name = "Test"
        type.processing = randomConfig.RandomDataTypeConf()
        type.processing.randElemCount = 1
        type.itemsType = model.StringType()

        ret = randomFuncs.generateRandomData(type, defaultConfig)
        self.assertTrue(isinstance(ret, list))
        self.assertTrue(len(ret) > 0)
        for r in ret:
            self.assertTrue(len(r) > 0)
            self.assertTrue(isinstance(r, str))

    def testArrayType2(self):
        defaultConfig = randomConfig.RamdonDefaultConfig()

        type = model.ArrayType()
        type.name = "Test"
        type.processing = randomConfig.RandomDataTypeConf()
        type.processing.randMinElemCount = 10
        type.processing.randMaxElemCount = 100
        type.itemsType = model.StringType()

        i = 0
        ok = False
        while i < 10:
            ret = randomFuncs.generateRandomData(type, defaultConfig)
            self.assertTrue(isinstance(ret, list))
            lRet = len(ret)
            if (lRet > 10) and (lRet < 100):
                ok = True
                break
            i = i + 1
        self.assertTrue(ok)
        pass

    def testArrayType3(self):
        defaultConfig = randomConfig.RamdonDefaultConfig()
        defaultConfig.defaultMinArrayElemCount = 3
        defaultConfig.defaultMaxArrayElemCount = 3

        type = model.ArrayType()
        type.name = "Test"
        type.processing = randomConfig.RandomDataTypeConf()
        type.processing.randElemCount = 1
        type.itemsType = model.IntegerType()

        ret = randomFuncs.generateRandomData(type, defaultConfig)
        self.assertTrue(isinstance(ret, list))
        self.assertEqual(len(ret), 3)
        for r in ret:
            self.assertTrue(isinstance(r, int))

    def testArrayType4(self):
        defaultConfig = randomConfig.RamdonDefaultConfig()
        defaultConfig.defaultMinArrayElemCount = 3
        defaultConfig.defaultMaxArrayElemCount = 3

        type = model.ArrayType()
        type.name = "Test"
        type.processing = randomConfig.RandomDataTypeConf()
        type.processing.randElemCount = 6
        type.itemsType = model.NumberType()

        ret = randomFuncs.generateRandomData(type, defaultConfig)
        self.assertTrue(isinstance(ret, list))
        self.assertEqual(len(ret), 6)
        for r in ret:
            self.assertTrue(isinstance(r, list))
            self.assertEqual(len(r), 3)

    def testDictionaryType1(self):
        defaultConfig = randomConfig.RamdonDefaultConfig()

        type = model.DictionaryType()
        type.name = "Test"
        type.processing = randomConfig.RandomDataTypeConf()
        type.processing.randElemCount = 1
        type.valueType = model.BooleanType()

        ret = randomFuncs.generateRandomData(type, defaultConfig)
        pass

    def testDictionaryType2(self):
        defaultConfig = randomConfig.RamdonDefaultConfig()

        type = model.DictionaryType()
        type.name = "Test"
        type.processing = randomConfig.RandomDataTypeConf()
        type.processing.randElemCount = 1

        type.valueType = model.ComplexType()
        prop = model.Property()
        prop.name = "myInt"
        prop.type = model.IntegerType()
        prop.required = True
        prop2 = model.Property()
        prop2.name = "myString"
        prop2.type = model.StringType()
        prop2.required = True
        type.valueType.properties.append(prop)
        type.valueType.properties.append(prop2)

        ret = randomFuncs.generateRandomData(type, defaultConfig)
        self.assertTrue(isinstance(ret, dict))
        pass

    def testMainFunc(self):
        args = createRandomData.Args()
        args.model = "resources/models/json/yacg_config_schema.json"
        args.outputDir = "tmp"
        args.type.append("Job")
        args.defaultElemCount = 1
        createRandomData.main(args)

    def testMainFunc2(self):
        args = createRandomData.Args()
        args.model = "tests/resources/models/yaml/examples/layer.yaml"
        args.outputDir = "tmp"
        args.type.append("LayerContent")
        args.defaultElemCount = 5
        args.defaultTypeDepth = 10
        args.defaultMinArrayElemCount = 1
        args.defaultMaxArrayElemCount = 5
        createRandomData.main(args)


    def testMainFunc(self):
        args = createRandomData.Args()
        args.model = "tests/resources/models/json/examples/nibelheim.json"
        args.outputDir = "tmp"
        args.type.append("History")
        args.defaultElemCount = 1
        createRandomData.main(args)
