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
