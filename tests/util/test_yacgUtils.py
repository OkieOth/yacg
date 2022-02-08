import unittest
import yacg.util.yacg_utils as yacg_utils


class TestYacgUtils (unittest.TestCase):
    def testGetJobConfigurationsFromConfigFile(self):
        jobArray = yacg_utils.getJobConfigurationsFromConfigFile('resources/configurations/gen_yacg_code.json')
        self.assertIsNotNone(jobArray)
        self.assertEqual(3, len(jobArray))
        self.assertEqual(1, len(jobArray[0].models))
        self.assertEqual(3, len(jobArray[0].tasks))
        self.assertEqual(1, len(jobArray[1].models))
        self.assertEqual(3, len(jobArray[1].tasks))
        self.assertEqual(1, len(jobArray[2].models))
        self.assertEqual(3, len(jobArray[2].tasks))

    def testGetJobConfigurationsFromConfigFileWithVarReplace(self):
        varDict = {
            'modelPath': 'resources/models',
            'modelFile': 'yacg_model_schema',
            'language': 'python',
            'destFile': 'model.py',
            'tmpDir': 'tmp',
            'modelPackage': 'de.vars.model'
        }
        jobArray = yacg_utils.getJobConfigurationsFromConfigFile(
            'resources/configurations/conf_with_vars.json',
            varDict)
        self.assertIsNotNone(jobArray)
        self.assertEqual(3, len(jobArray))
        self.assertEqual(1, len(jobArray[0].models))
        self.assertEqual('resources/models/json/yacg_model_schema.json', jobArray[0].models[0].schema)
        self.assertEqual(
            'pythonBeans',
            jobArray[0].tasks[0].singleFileTask.template)
        self.assertEqual(
            'tmp/model.py',
            jobArray[0].tasks[0].singleFileTask.destFile)
        self.assertEqual(
            'tmp/javaBeans2',
            jobArray[0].tasks[1].multiFileTask.destDir)
        self.assertEqual(
            'de.vars.model',
            jobArray[0].tasks[1].multiFileTask.templateParams[0].value)

        self.assertEqual(2, len(jobArray[0].tasks))
        self.assertEqual(1, len(jobArray[1].models))
        self.assertEqual(3, len(jobArray[1].tasks))
        self.assertEqual(1, len(jobArray[2].models))
        self.assertEqual(3, len(jobArray[2].tasks))

    def testGetVarList(self):
        result1 = yacg_utils.getVarList('i{Am}AString{With}Variables')
        self.assertEqual(2, len(result1))
        self.assertEqual('Am', result1[0])
        self.assertEqual('With', result1[1])

        result2 = yacg_utils.getVarList('{TEST}i{AM}AString{With}Variables{}')
        self.assertEqual(3, len(result2))
        self.assertEqual('TEST', result2[0])
        self.assertEqual('AM', result2[1])
        self.assertEqual('With', result2[2])

        result3 = yacg_utils.getVarList('{TEST}i{AM}AString{With}{y}Variables{XXX}')
        self.assertEqual(5, len(result3))
        self.assertEqual('TEST', result3[0])
        self.assertEqual('AM', result3[1])
        self.assertEqual('With', result3[2])
        self.assertEqual('y', result3[3])
        self.assertEqual('XXX', result3[4])

    def testReplaceVar(self):
        result1 = yacg_utils.replaceVar('i{Am}AString{With}Variables', 'Am', 'AM')
        self.assertEqual('iAMAString{With}Variables', result1)

    def testGetConfigJobsCmdLineSwitch1(self):
        jobsToInclude = ["config_types"]
        jobArray = yacg_utils.getJobConfigurationsFromConfigFile(
            'resources/configurations/gen_yacg_code.json',
            {}, jobsToInclude)
        self.assertIsNotNone(jobArray)
        self.assertEqual(1, len(jobArray))
        self.assertEqual("config_types", jobArray[0].name)

    def testGetConfigJobsCmdLineSwitch2(self):
        jobsToInclude = ["config_types", "openapi_types"]
        jobArray = yacg_utils.getJobConfigurationsFromConfigFile(
            'resources/configurations/gen_yacg_code.json',
            {}, jobsToInclude)
        self.assertIsNotNone(jobArray)
        self.assertEqual(2, len(jobArray))
        self.assertEqual("config_types", jobArray[0].name)
        self.assertEqual("openapi_types", jobArray[1].name)

    def testGetConfigTasksCmdLineSwitch1(self):
        tasksToInclude = ["puml", "python_types"]
        jobArray = yacg_utils.getJobConfigurationsFromConfigFile(
            'resources/configurations/gen_yacg_code.json',
            {}, (), tasksToInclude)
        self.assertIsNotNone(jobArray)
        self.assertEqual(3, len(jobArray))
        self.assertEqual(2, len(jobArray[0].tasks))
        self.assertEqual(2, len(jobArray[1].tasks))
        self.assertEqual(2, len(jobArray[2].tasks))
        self.assertEqual("python_types", jobArray[0].tasks[0].name)
        self.assertEqual("python_types", jobArray[1].tasks[0].name)
        self.assertEqual("python_types", jobArray[2].tasks[0].name)
        self.assertEqual("puml", jobArray[0].tasks[1].name)
        self.assertEqual("puml", jobArray[1].tasks[1].name)
        self.assertEqual("puml", jobArray[2].tasks[1].name)
