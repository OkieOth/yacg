import unittest
from pathlib import Path
import shutil
import os
import modelToYaml
from yacg.util.fileUtils import doesFileExist


class TestModelToYaml (unittest.TestCase):
    def testTrimFileName(self):
        ret = modelToYaml._trimModelFileName('test/test2/tttt.json')
        self.assertEqual('tttt', ret)
        ret = modelToYaml._trimModelFileName('test/test2/ttty.yaml')
        self.assertEqual('ttty', ret)
        ret = modelToYaml._trimModelFileName('test/test2/tttz.yaml')
        self.assertFalse('ttty' == ret)

    def testDryRun(self):
        model = 'resources/models/json/yacg_config_schema.json'
        modelToYaml._convertModel(model, True, 'dummy')

    def testConvertFile(self):
        dirpath = Path('tmp', 'model2yaml')
        if dirpath.exists() and dirpath.is_dir():
            shutil.rmtree(dirpath)
        os.mkdir(dirpath)
        model = 'resources/models/json/yacg_config_schema.json'
        modelToYaml._convertModel(model, False, 'tmp/model2yaml')
        self.assertTrue(doesFileExist('tmp/model2yaml/yacg_config_schema.yaml'))

if __name__ == '__main__':
    unittest.main()
