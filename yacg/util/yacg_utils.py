import json
import yaml
import yacg.model.config as config
import re
import os

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
            varList = getVarList(modelFile.schema)            
            for varName in varList:
                varValue = resolvVar(varName)
                modelFile.schema = replaceVar(modelFile.schema, varName, varValue)
        for task in job.tasks:
            if task.singleFileTask is not None:
                template = task.singleFileTask.template
                varListTemplate = getVarList(template)
                for varName in varListTemplate:
                    varValue = resolvVar(varName)
                    task.singleFileTask.template = replaceVar(task.singleFileTask.template, varName, varValue)
                varListDestFile = getVarList(task.singleFileTask.destFile)
                for varName in varListDestFile:
                    varValue = resolvVar(varName)
                    task.singleFileTask.destFile = replaceVar(task.singleFileTask.destFile, varName, varValue)
                _replaceVarsInTemplateParamValues(task.singleFileTask.templateParams)
            if task.multiFileTask is not None:
                template = task.multiFileTask.template
                varList = getVarList(template)
                for varName in varList:
                    varValue = resolvVar(varName)
                    task.multiFileTask.template = replaceVar(task.multiFileTask.template, varName, varValue)
                varListDestDir = getVarList(task.multiFileTask.destDir)
                for varName in varListDestDir:
                    varValue = resolvVar(varName)
                    task.multiFileTask.destDir = replaceVar(task.multiFileTask.destDir, varName, varValue)
                _replaceVarsInTemplateParamValues(task.multiFileTask.templateParams)


def _replaceVarsInTemplateParamValues(templateParams):
    for param in templateParams:
        varList = getVarList(param.value)
        for varName in varList:
            varValue = resolvVar(varName)
            param.value = replaceVar(param.value, varName, varValue)


def resolvVar(varName):
    varValue = os.environ.get(varName, '>>ENV_VAR {} NOT SET<<'.format(varName))
    return varValue


def replaceVar(strToProcess, varName, varValue):
    strToReplace = '{' + varName + '}'
    return strToProcess.replace(strToReplace, varValue, 1)


def getVarList(strLine):
    """this function takes a string in the format 'i{Am}AString{With}Variables'
    and parse it for included var entries '{.+}'. The return of the function in
    case of the example would be: ('Am','With')
    """

    result = []
    if strLine is None:
        return result
    pattern = re.compile('{[a-zA-Z]+}')
    matchList = pattern.findall(strLine);
    for match in matchList:
        result.append(match[1:-1])
    return result
