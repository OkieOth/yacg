import json
import yaml
import yacg.model.config as config
import re
import os

from yacg.util.fileUtils import doesFileExist
from yacg.util.outputUtils import printError


def getJobConfigurationsFromConfigFile(configFile, additionalVarsDict={}, jobsToInclude=[], tasksToInclude=[]):
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
        job = config.Job(conf)
        if (len(jobsToInclude) > 0) and (job.name not in jobsToInclude):
            continue
        __removeUndesiredTasksIfNeeded(tasksToInclude, job)
        jobArray.append(job)
    __replaceEnvVars(jobArray, additionalVarsDict)
    return jobArray


def __removeUndesiredTasksIfNeeded(tasksToInclude, job):
    if len(tasksToInclude) > 0:
        tasksFromConfig = job.tasks
        job.tasks = []
        for task in tasksFromConfig:
            if task.name in tasksToInclude:
                job.tasks.append(task)


def __replaceEnvVars(jobArray, additionalVarsDict):
    """walks through the configuration and replace env var placeholders"""

    for job in jobArray:
        for index in range(len(job.models)):
            modelFile = job.models[index]
            varList = getVarList(modelFile.schema)
            for varName in varList:
                varValue = resolveVar(varName, additionalVarsDict)
                modelFile.schema = replaceVar(modelFile.schema, varName, varValue)
        for task in job.tasks:
            if task.singleFileTask is not None:
                __replaceEnvVarsInSingleFileTask(task.singleFileTask, additionalVarsDict)
            if task.multiFileTask is not None:
                __replaceEnvVarsInMultiFileTask(task.multiFileTask, additionalVarsDict)
            # not needed for randomDataTask


def __replaceEnvVarsInSingleFileTask(singleFileTask, additionalVarsDict):
    template = singleFileTask.template
    varListTemplate = getVarList(template)
    for varName in varListTemplate:
        varValue = resolveVar(varName, additionalVarsDict)
        singleFileTask.template = replaceVar(singleFileTask.template, varName, varValue)
    varListDestFile = getVarList(singleFileTask.destFile)
    for varName in varListDestFile:
        varValue = resolveVar(varName, additionalVarsDict)
        singleFileTask.destFile = replaceVar(singleFileTask.destFile, varName, varValue)
    _replaceVarsInTemplateParamValues(singleFileTask.templateParams, additionalVarsDict)


def __replaceEnvVarsInMultiFileTask(multiFileTask, additionalVarsDict):
    template = multiFileTask.template
    varList = getVarList(template)
    for varName in varList:
        varValue = resolveVar(varName, additionalVarsDict)
        multiFileTask.template = replaceVar(multiFileTask.template, varName, varValue)
    varListDestDir = getVarList(multiFileTask.destDir)
    for varName in varListDestDir:
        varValue = resolveVar(varName, additionalVarsDict)
        multiFileTask.destDir = replaceVar(multiFileTask.destDir, varName, varValue)
    _replaceVarsInTemplateParamValues(multiFileTask.templateParams, additionalVarsDict)


def _replaceVarsInTemplateParamValues(templateParams, additionalVarsDict):
    for param in templateParams:
        varList = getVarList(param.value)
        for varName in varList:
            varValue = resolveVar(varName, additionalVarsDict)
            param.value = replaceVar(param.value, varName, varValue)


def resolveVar(varName, additionalVarsDict):
    varValue = os.environ.get(varName, None)
    if (varValue is None) or (len(varValue) == 0):
        varValue = additionalVarsDict.get(varName, '>>VAR {} NOT SET<<'.format(varName))
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
    matchList = pattern.findall(strLine)
    for match in matchList:
        result.append(match[1:-1])
    return result
