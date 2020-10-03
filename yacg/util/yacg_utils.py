import json
import yaml
import yacg.model.config as config
import re

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
    __replaceEnvVars(jobArray)
    return jobArray

def __replaceEnvVars(jobArray):
    """walks through the configuration and replace env var placeholders"""

    for job in jobArray:
        for index in range(len(job.models)):
            modelFile = job.models[index]
            # toto extract env vars
            pass 
    pass


def getVarList(strLine):
    """this function takes a string in the format 'i{Am}AString{With}Variables'
    and parse it for included var entries '{.+}'. The return of the function in
    case of the example would be: ('Am','With')
    """

    result = []
    pattern = re.compile('{[a-zA-Z]+}')
    matchList = pattern.findall(strLine);
    for match in matchList:
        result.append(match[1:-1])
    return result
