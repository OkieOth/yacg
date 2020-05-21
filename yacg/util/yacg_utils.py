import json
import yaml
import yacg.model.config as config

from yacg.util.fileUtils import doesFileExist
from yacg.util.outputUtils import printError


def getJobConfigurationsFromConfigFile(configFile):
    if not doesFileExist(configFile):
        printError('\ncan not find config file: {}'.format(configFile))
        return []
    configurations = None
    if configFile.endswith('.json'):
        with open(configFile) as configFileContent:
            configurations = json.load(configFileContent)
    elif configFile.endswith('.yaml') or configFile.endswith('.yaml'):
        with open(configFile) as configFileContent:
            configurations = yaml.load(configFileContent)
    else:
        printError('\nunknown config file extension, only json or yaml are supportted')
        return []
    jobArray = []
    for conf in configurations:
        job = config.Job.dictToObject(conf)
        jobArray.append(job)
    return jobArray
