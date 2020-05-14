# Attention, this file is generated. Manual changes get lost with the next
# run of the code generation.
# created by yacg (template: pythonBeans.mako v1.0.0)

import unittest

from <<"modelPackage" template param is missing>> import PathType
from <<"modelPackage" template param is missing>> import Command
from <<"modelPackage" template param is missing>> import CommandCommandEnum
from <<"modelPackage" template param is missing>> import Parameter
from <<"modelPackage" template param is missing>> import RequestBody
from <<"modelPackage" template param is missing>> import Response
from <<"modelPackage" template param is missing>> import ContentEntry
from <<"modelPackage" template param is missing>> import ParameterInTypeEnum


class TestYacgOpenapiModel (unittest.TestCase):
    def testPathType(self):
        x = PathType()
        self.assertIsNotNone(x)

    def testCommand(self):
        x = Command()
        self.assertIsNotNone(x)

    def testCommandCommandEnum(self):
        self.assertIsNotNone(CommandCommandEnum.GET)
        self.assertIsNotNone(CommandCommandEnum.PUT)
        self.assertIsNotNone(CommandCommandEnum.POST)
        self.assertIsNotNone(CommandCommandEnum.DELETE)
        self.assertIsNotNone(CommandCommandEnum.OPTIONS)

    def testParameter(self):
        x = Parameter()
        self.assertIsNotNone(x)

    def testRequestBody(self):
        x = RequestBody()
        self.assertIsNotNone(x)

    def testResponse(self):
        x = Response()
        self.assertIsNotNone(x)

    def testContentEntry(self):
        x = ContentEntry()
        self.assertIsNotNone(x)

    def testParameterInTypeEnum(self):
        self.assertIsNotNone(ParameterInTypeEnum.PATH)
        self.assertIsNotNone(ParameterInTypeEnum.QUERY)
        self.assertIsNotNone(ParameterInTypeEnum.HEADER)
        self.assertIsNotNone(ParameterInTypeEnum.COOKIE)


if __name__ == '__main__':
    unittest.main()
