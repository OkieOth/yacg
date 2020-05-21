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

    def testSingleFileTask(self):
        x = yacg.model.config.SingleFileTask()
        self.assertIsNotNone(x)

    def testTemplateParam(self):
        x = yacg.model.config.TemplateParam()
        self.assertIsNotNone(x)

    def testMultiFileTask(self):
        x = yacg.model.config.MultiFileTask()
        self.assertIsNotNone(x)


if __name__ == '__main__':
    unittest.main()
