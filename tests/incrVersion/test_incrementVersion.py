import unittest

import incrementVersion
from yacg.util.fileUtils import doesFileExist


class TestIncrementVersion (unittest.TestCase):
    def testSemver(self):
        ret = incrementVersion._checkValidVersion('1.3.4')
        self.assertTrue(ret)
        ret = incrementVersion._checkValidVersion('xxx')
        self.assertFalse(ret)

    def testGetJsonSchemaFileNames(self):
        ret = incrementVersion._getJsonSchemaFileNames('./resources')
        self.assertEqual(8, len(ret))
        for file in ret:
            self.assertTrue(doesFileExist(file))
        ret2 = incrementVersion._getJsonSchemaFileNames('./tests')
        self.assertEqual(20, len(ret2))
        for file in ret2:
            self.assertTrue(doesFileExist(file))
        # negative test
        self.assertFalse(doesFileExist(ret2[0] + "xx"))


if __name__ == '__main__':
    unittest.main()
