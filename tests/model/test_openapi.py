# Attention, this file is generated. Manual changes get lost with the next
# run of the code generation.
# created by yacg (template: pythonBeans.mako v1.0.0)

import unittest

from yacg.model.openapi import PathType
from yacg.model.openapi import Command
from yacg.model.openapi import CommandCommandEnum
from yacg.model.openapi import CommandConsumesEnum
from yacg.model.openapi import CommandProducesEnum
from yacg.model.openapi import Parameter
from yacg.model.openapi import RequestBody
from yacg.model.openapi import Response
from yacg.model.openapi import RequestBodyContent
from yacg.model.openapi import ParameterInTypeEnum


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

    def testCommandConsumesEnum(self):
        self.assertIsNotNone(CommandConsumesEnum.APPLICATION_JSON)
        self.assertIsNotNone(CommandConsumesEnum.APPLICATION_XML)

    def testCommandProducesEnum(self):
        self.assertIsNotNone(CommandProducesEnum.APPLICATION_JSON)
        self.assertIsNotNone(CommandProducesEnum.APPLICATION_XML)

    def testParameter(self):
        x = Parameter()
        self.assertIsNotNone(x)

    def testRequestBody(self):
        x = RequestBody()
        self.assertIsNotNone(x)

    def testResponse(self):
        x = Response()
        self.assertIsNotNone(x)

    def testRequestBodyContent(self):
        x = RequestBodyContent()
        self.assertIsNotNone(x)

    def testParameterInTypeEnum(self):
        self.assertIsNotNone(ParameterInTypeEnum.PATH)
        self.assertIsNotNone(ParameterInTypeEnum.QUERY)
        self.assertIsNotNone(ParameterInTypeEnum.HEADER)
        self.assertIsNotNone(ParameterInTypeEnum.COOKIE)


if __name__ == '__main__':
    unittest.main()
