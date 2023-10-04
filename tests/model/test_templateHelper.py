import unittest

import yacg.templateHelper as templateHelper


# For executing these test run: python -m unittest -v tests/model/test_templateHelper.py
class TestTemplateHelper (unittest.TestCase):

    def testAddLineBreakToDesc(self):
        input = 'abc def'

        act = templateHelper.addLineBreakToDescription(input, 0)
        self.assertEqual(act, 'abc def')

        act = templateHelper.addLineBreakToDescription(input, 4)
        self.assertEqual(act, 'abc def')

        act = templateHelper.addLineBreakToDescription(input, 0, '// ')
        self.assertEqual(act, '// abc def')

        act = templateHelper.addLineBreakToDescription(input, 4, '// ')
        self.assertEqual(act, '// abc def')

        # line break is inserted when token starts after more than 60 (none white space) characters were already processed
        input = '0123456789 0123456789 0123456789 0123456789 0123456789 0123456789abc 0123456789'
        act = templateHelper.addLineBreakToDescription(input, 0)
        self.assertEqual(act, '0123456789 0123456789 0123456789 0123456789 0123456789 0123456789abc\n0123456789')

        act = templateHelper.addLineBreakToDescription(input, 4)
        self.assertEqual(act, '0123456789 0123456789 0123456789 0123456789 0123456789 0123456789abc\n    0123456789')

        input = '0123456789 0123456789 0123456789 0123456789 0123456789 0123456789abc 0123456789'
        act = templateHelper.addLineBreakToDescription(input, 0, '// ')
        self.assertEqual(act, '// 0123456789 0123456789 0123456789 0123456789 0123456789 0123456789abc\n// 0123456789')

        input = '0123456789 0123456789 0123456789 0123456789 0123456789 0123456789abc 0123456789'
        act = templateHelper.addLineBreakToDescription(input, 4, '// ')
        self.assertEqual(act, '// 0123456789 0123456789 0123456789 0123456789 0123456789 0123456789abc\n    // 0123456789')
