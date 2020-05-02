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

        
