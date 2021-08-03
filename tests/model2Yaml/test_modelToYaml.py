import unittest
from pathlib import Path
import shutil
import os
import json
from modelToYaml import trimModelFileName, convertModel, traverseDictAndReplaceRefExtensions
from yacg.util.fileUtils import doesFileExist


class TestModelToYaml (unittest.TestCase):
    def testTrimFileName(self):
        ret = trimModelFileName('test/test2/tttt.json')
        self.assertEqual('tttt', ret)
        ret = trimModelFileName('test/test2/ttty.yaml')
        self.assertEqual('ttty', ret)
        ret = trimModelFileName('test/test2/tttz.yaml')
        self.assertFalse('ttty' == ret)

    def __testDryRun(self):
        # this test blurs to test output
        model = 'resources/models/json/yacg_config_schema.json'
        convertModel(model, True, 'dummy')

    def testConvertFile(self):
        dirpath = Path('tmp', 'model2yaml')
        if dirpath.exists() and dirpath.is_dir():
            shutil.rmtree(dirpath)
        os.mkdir(dirpath)
        model = 'resources/models/json/yacg_config_schema.json'
        convertModel(model, False, 'tmp/model2yaml')
        self.assertTrue(doesFileExist('tmp/model2yaml/yacg_config_schema.yaml'))

    def testTraverseDictAndReplaceRefExtensions(self):
        with open('tests/resources/models/json/examples/more_sophisticated_allof.json') as openFile:
            content = json.load(openFile)
            str1 = str(content)
            jsonCount1 = str1.count('.json')
            yamlCount1 = str1.count('.yaml')
            self.assertEqual(2, jsonCount1)
            self.assertEqual(0, yamlCount1)
            print('jsonCount1={}, yamlCount1={}'.format(jsonCount1, yamlCount1))
            traverseDictAndReplaceRefExtensions(content, True)
            str2 = str(content)
            jsonCount2 = str2.count('.json')
            yamlCount2 = str2.count('.yaml')
            self.assertEqual(0, jsonCount2)
            self.assertEqual(jsonCount1, yamlCount2)

    def testTraverseDictAndReplaceRefExtensions2(self):
        with open('tests/resources/models/json/examples/more_sophisticated_allof.json') as openFile:
            content = json.load(openFile)
            str1 = str(content)
            jsonCount1 = str1.count('.json')
            yamlCount1 = str1.count('.yaml')
            self.assertEqual(2, jsonCount1)
            self.assertEqual(0, yamlCount1)
            print('jsonCount1={}, yamlCount1={}'.format(jsonCount1, yamlCount1))
            traverseDictAndReplaceRefExtensions(content, False)
            str2 = str(content)
            jsonCount2 = str2.count('.json')
            yamlCount2 = str2.count('.yaml')
            self.assertEqual(2, jsonCount2)
            self.assertEqual(0, yamlCount2)


if __name__ == '__main__':
    unittest.main()
