# Attention, this file is generated. Manual changes get lost with the next
# run of the code generation.
# created by yacg (template: pythonBeans.mako v1.0.0)

import unittest

from yacg.model.config import Job
from yacg.model.config import Model
from yacg.model.config import Task
from yacg.model.config import BlackWhiteListEntry
from yacg.model.config import BlackWhiteListEntryTypeEnum
from yacg.model.config import SingleFileTask
from yacg.model.config import TemplateParam
from yacg.model.config import MultiFileTask


class TestYacgConfigurationModel (unittest.TestCase):
    def testJob(self):
        x = Job()
        self.assertIsNotNone(x)

    def testModel(self):
        x = Model()
        self.assertIsNotNone(x)

    def testTask(self):
        x = Task()
        self.assertIsNotNone(x)

    def testBlackWhiteListEntry(self):
        x = BlackWhiteListEntry()
        self.assertIsNotNone(x)

    def testBlackWhiteListEntryTypeEnum(self):
        self.assertIsNotNone(BlackWhiteListEntryTypeEnum.TYPE)
        self.assertIsNotNone(BlackWhiteListEntryTypeEnum.TAG)
        self.assertIsNotNone(BlackWhiteListEntryTypeEnum.CONTAINEDATTRIB)
        self.assertIsNotNone(BlackWhiteListEntryTypeEnum.NOTCONTAINEDATTRIB)
        self.assertIsNotNone(BlackWhiteListEntryTypeEnum.DOMAIN)

    def testSingleFileTask(self):
        x = SingleFileTask()
        self.assertIsNotNone(x)

    def testTemplateParam(self):
        x = TemplateParam()
        self.assertIsNotNone(x)

    def testMultiFileTask(self):
        x = MultiFileTask()
        self.assertIsNotNone(x)


if __name__ == '__main__':
    unittest.main()
