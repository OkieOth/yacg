# Attention, this file is generated. Manual changes get lost with the next
# run of the code generation.
# created by yacg (template: pythonBeans.mako v1.0.0)

import unittest

import yacg.model.openapi
import yacg.model.model


class TestYacgOpenapiModel (unittest.TestCase):
    def testPathType(self):
        x = yacg.model.openapi.PathType()
        self.assertIsNotNone(x)

    def testCommand(self):
        x = yacg.model.openapi.Command()
        self.assertIsNotNone(x)

    def testCommandCommandEnum(self):
        self.assertIsNotNone(yacg.model.openapi.CommandCommandEnum.GET)
        self.assertIsNotNone(yacg.model.openapi.CommandCommandEnum.PUT)
        self.assertIsNotNone(yacg.model.openapi.CommandCommandEnum.POST)
        self.assertIsNotNone(yacg.model.openapi.CommandCommandEnum.DELETE)
        self.assertIsNotNone(yacg.model.openapi.CommandCommandEnum.OPTIONS)

    def testParameter(self):
        x = yacg.model.openapi.Parameter()
        self.assertIsNotNone(x)

    def testRequestBody(self):
        x = yacg.model.openapi.RequestBody()
        self.assertIsNotNone(x)

    def testResponse(self):
        x = yacg.model.openapi.Response()
        self.assertIsNotNone(x)

    def testContentEntry(self):
        x = yacg.model.openapi.ContentEntry()
        self.assertIsNotNone(x)

    def testParameterInTypeEnum(self):
        self.assertIsNotNone(yacg.model.openapi.ParameterInTypeEnum.PATH)
        self.assertIsNotNone(yacg.model.openapi.ParameterInTypeEnum.QUERY)
        self.assertIsNotNone(yacg.model.openapi.ParameterInTypeEnum.HEADER)
        self.assertIsNotNone(yacg.model.openapi.ParameterInTypeEnum.COOKIE)


if __name__ == '__main__':
    unittest.main()
