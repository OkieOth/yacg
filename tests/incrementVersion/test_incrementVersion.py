# Attention, this file is generated. Manual changes get lost with the next
# run of the code generation.
# created by yacg (template: pythonBeans.mako v1.0.0)

import unittest

import incrementVersion


class TestIncrementVersion (unittest.TestCase):
    def testSemver(self):
        ret = incrementVersion._checkValidVersion('1.3.4')
        self.assertTrue(ret)
        ret = incrementVersion._checkValidVersion('xxx')
        self.assertFalse(ret)



if __name__ == '__main__':
    unittest.main()
