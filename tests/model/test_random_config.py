# Attention, this file is generated. Manual changes get lost with the next
# run of the code generation.
# created by yacg (template: pythonBeans.mako v1.0.0)

import unittest

import yacg.model.random_config


class TestYacgConfigurationForRandomDataGeneration (unittest.TestCase):
    def testRamdonDefaultConfig(self):
        x = yacg.model.random_config.RamdonDefaultConfig()
        self.assertIsNotNone(x)

    def testRandomDataTypeConf(self):
        x = yacg.model.random_config.RandomDataTypeConf()
        self.assertIsNotNone(x)

    def testRandomDataPropertyConf(self):
        x = yacg.model.random_config.RandomDataPropertyConf()
        self.assertIsNotNone(x)

    def testRandomArrayConf(self):
        x = yacg.model.random_config.RandomArrayConf()
        self.assertIsNotNone(x)

    def testRandomPropertyTypeConf(self):
        x = yacg.model.random_config.RandomPropertyTypeConf()
        self.assertIsNotNone(x)

    def testRandomComplexTypeConf(self):
        x = yacg.model.random_config.RandomComplexTypeConf()
        self.assertIsNotNone(x)

    def testRandomStringTypeConf(self):
        x = yacg.model.random_config.RandomStringTypeConf()
        self.assertIsNotNone(x)

    def testRandomNumTypeConf(self):
        x = yacg.model.random_config.RandomNumTypeConf()
        self.assertIsNotNone(x)

    def testRandomDateTypeConf(self):
        x = yacg.model.random_config.RandomDateTypeConf()
        self.assertIsNotNone(x)

    def testRandomTimeTypeConf(self):
        x = yacg.model.random_config.RandomTimeTypeConf()
        self.assertIsNotNone(x)

    def testRandomDurationTypeConf(self):
        x = yacg.model.random_config.RandomDurationTypeConf()
        self.assertIsNotNone(x)

    def testRandomStringTypeConfStrTypeEnum(self):
        self.assertIsNotNone(yacg.model.random_config.RandomStringTypeConfStrTypeEnum.NAME)
        self.assertIsNotNone(yacg.model.random_config.RandomStringTypeConfStrTypeEnum.ADDRESS)
        self.assertIsNotNone(yacg.model.random_config.RandomStringTypeConfStrTypeEnum.EMAIL)
        self.assertIsNotNone(yacg.model.random_config.RandomStringTypeConfStrTypeEnum.URL)
        self.assertIsNotNone(yacg.model.random_config.RandomStringTypeConfStrTypeEnum.PHONE)
        self.assertIsNotNone(yacg.model.random_config.RandomStringTypeConfStrTypeEnum.COUNTRY)
        self.assertIsNotNone(yacg.model.random_config.RandomStringTypeConfStrTypeEnum.TEXT)
        self.assertIsNotNone(yacg.model.random_config.RandomStringTypeConfStrTypeEnum.SENTENCE)


if __name__ == '__main__':
    unittest.main()
