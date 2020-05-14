# Attention, this file is generated. Manual changes get lost with the next
# run of the code generation.
# created by yacg (template: pythonBeans.mako v1.0.0)

import unittest

from <<"modelPackage" template param is missing>> import Job
from <<"modelPackage" template param is missing>> import Model
from <<"modelPackage" template param is missing>> import Task
from <<"modelPackage" template param is missing>> import BlackWhiteListEntry
from <<"modelPackage" template param is missing>> import BlackWhiteListEntryTypeEnum
from <<"modelPackage" template param is missing>> import SingleFileTask
from <<"modelPackage" template param is missing>> import TemplateParam
from <<"modelPackage" template param is missing>> import MultiFileTask


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
