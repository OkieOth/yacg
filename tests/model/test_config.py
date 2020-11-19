# Attention, this file is generated. Manual changes get lost with the next
# run of the code generation.
# created by yacg (template: pythonBeans.mako v1.0.0)

import unittest

import yacg.model.config


class TestYacgConfigurationModel (unittest.TestCase):
    def testJob(self):
        x = yacg.model.config.Job()
        self.assertIsNotNone(x)

    def testModel(self):
        x = yacg.model.config.Model()
        self.assertIsNotNone(x)

    def testTask(self):
        x = yacg.model.config.Task()
        self.assertIsNotNone(x)

    def testBlackWhiteListEntry(self):
        x = yacg.model.config.BlackWhiteListEntry()
        self.assertIsNotNone(x)

    def testBlackWhiteListEntryTypeEnum(self):
        self.assertIsNotNone(yacg.model.config.BlackWhiteListEntryTypeEnum.TYPE)
        self.assertIsNotNone(yacg.model.config.BlackWhiteListEntryTypeEnum.TAG)
        self.assertIsNotNone(yacg.model.config.BlackWhiteListEntryTypeEnum.CONTAINEDATTRIB)
        self.assertIsNotNone(yacg.model.config.BlackWhiteListEntryTypeEnum.NOTCONTAINEDATTRIB)
        self.assertIsNotNone(yacg.model.config.BlackWhiteListEntryTypeEnum.DOMAIN)
        self.assertIsNotNone(yacg.model.config.BlackWhiteListEntryTypeEnum.TYPETYPE)

    def testSingleFileTask(self):
        x = yacg.model.config.SingleFileTask()
        self.assertIsNotNone(x)

    def testTemplateParam(self):
        x = yacg.model.config.TemplateParam()
        self.assertIsNotNone(x)

    def testMultiFileTask(self):
        x = yacg.model.config.MultiFileTask()
        self.assertIsNotNone(x)

    def testMultiFileTaskFileFilterTypeEnum(self):
        self.assertIsNotNone(yacg.model.config.MultiFileTaskFileFilterTypeEnum.TYPE)
        self.assertIsNotNone(yacg.model.config.MultiFileTaskFileFilterTypeEnum.OPENAPIOPERATIONID)

    def testRandomDataTask(self):
        x = yacg.model.config.RandomDataTask()
        self.assertIsNotNone(x)

    def testRandomDataTaskOutputTypeEnum(self):
        self.assertIsNotNone(yacg.model.config.RandomDataTaskOutputTypeEnum.JSON)
        self.assertIsNotNone(yacg.model.config.RandomDataTaskOutputTypeEnum.CSV)

    def testRandomDataTaskElemCount(self):
        x = yacg.model.config.RandomDataTaskElemCount()
        self.assertIsNotNone(x)

    def testRandomDataTaskElemCountSpecialElemCounts(self):
        x = yacg.model.config.RandomDataTaskElemCountSpecialElemCounts()
        self.assertIsNotNone(x)

    def testRandomDataTaskKeyProperties(self):
        x = yacg.model.config.RandomDataTaskKeyProperties()
        self.assertIsNotNone(x)

    def testRandomDataTaskKeyPropertiesSpecialKeyPropNames(self):
        x = yacg.model.config.RandomDataTaskKeyPropertiesSpecialKeyPropNames()
        self.assertIsNotNone(x)

    def testRandomDataTaskValuePools(self):
        x = yacg.model.config.RandomDataTaskValuePools()
        self.assertIsNotNone(x)

    def testRandomDataTaskArrays(self):
        x = yacg.model.config.RandomDataTaskArrays()
        self.assertIsNotNone(x)

    def testRandomDataTaskArraysSpecialArraySizes(self):
        x = yacg.model.config.RandomDataTaskArraysSpecialArraySizes()
        self.assertIsNotNone(x)


if __name__ == '__main__':
    unittest.main()
