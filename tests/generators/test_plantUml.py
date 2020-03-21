import unittest
import os.path
from mako.template import Template
from yacg.builder.jsonBuilder import getModelFromJson

class TestPlantUml (unittest.TestCase):
    def testSingleTypeSchema(self):
        modelFile = 'resources/models/json/examples/single_type_schema.json'
        modelFileExists = os.path.isfile(modelFile)
        self.assertTrue ('model file exists: '+ modelFile,modelFileExists)
        modelTypes = getModelFromJson (modelFile)
        templateFile = 'yacg/generators/templates/plantUml.mako'
        template = Template(filename=templateFile)
        templateFileExists = os.path.isfile(modelFile)
        self.assertTrue ('template file exists: '+ templateFile,templateFileExists)
        renderResult = template.render(modelTypes = modelTypes)
        self.assertIsNotNone(renderResult)

        testOutputFile = "tmp/singleTypeSchema.puml"
        f = open(testOutputFile,"w+")
        f.write(renderResult)
        f.close()
