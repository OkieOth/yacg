import unittest
import yacg.model.randomFuncs as randomFuncs
import yacg.model.random_config as randomConfig
import yacg.model.model as model


class TestRandomFuncs (unittest.TestCase):
    def test1(self):
        defaultConfig = randomConfig.RamdonDefaultConfig()

        type = model.ComplexType()
        type.name = "Test"
        type.processing = randomConfig.RandomDataTypeConf()
        type.processing.randElemCount = 1
        prop = model.Property()
        prop.name = "myInt"
        prop.type = model.IntegerType
        prop2 = model.Property()
        prop2.name = "myString"
        prop2.type = model.StringType
        type.properties.append(prop)
        type.properties.append(prop2)

        ret = randomFuncs.generateRandomData(type, defaultConfig)
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
        pass
