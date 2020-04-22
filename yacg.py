import argparse
import sys
import logging


from yacg.util.fileUtils import doesFileExist
from yacg.util.outputUtils import printError, getErrorTxt, getOkTxt
from yacg.builder.jsonBuilder import getModelFromJson
from yacg.builder.yamlBuilder import getModelFromYaml
from yacg.generators.singleFileGenerator import renderSingleFileTemplate

import yacg.model.config as config


description = """Yet another code generation.
Program takes one or more models, a bunch of templates and generates
source code from it
"""

logging.basicConfig(level=logging.INFO)

parser = argparse.ArgumentParser(prog='yacg', description=description)
parser.add_argument_group('input')
parser.add_argument('--models', nargs='+', help='models to process')
parser.add_argument('--config', nargs='?', help='config file')
parser.add_argument_group('processing')
parser.add_argument('--singleFileTemplates', nargs='+', help='templates to process that creates one file')
parser.add_argument('--multiFileTemplates', nargs='+', help='templates to process that creates one file per type')
parser.add_argument_group('additional')
parser.add_argument('--templateParameters', nargs='+', help='additional parameters passed to the templates')


def getFileExt(fileName):
    """returns the fileextension of a given file name"""

    lastDot = fileName.rindex('.')
    return fileName[lastDot:]


def readModels(configJob):
    """reads all desired models and build the model object tree from it"""

    loadedTypes = []
    yamlExtensions = set(['.yaml', '.yml'])
    for model in configJob.models:
        fileExt = getFileExt(model.schema)
        if fileExt.lower() in yamlExtensions:
            loadedTypes = getModelFromYaml(model, loadedTypes)
        else:
            loadedTypes = getModelFromJson(model, loadedTypes)
    return loadedTypes


def _getTemplateParameters(args):
    """extracts the per command line given template parameters, copies them
    into a dictionary and return this dictonary
    """

    templateParameters = {}
    for parameter in args.templateParameters:
        keyValueArray = parameter.split('=')
        if (len(keyValueArray) == 2):
            templateParameters[keyValueArray[0]] = keyValueArray[1]
        else:
            printError('\ntemplate param with wrong structure found ... skipped: {}'.format(parameter))
    return templateParameters


def _getJobConfigurationsFromConfigFile(configFile):
    # TODO
    return []


def _splitTemplateAndDestination(templateArg):
    keyValueArray = templateArg.split('=')
    if (len(keyValueArray) > 1):
        return (keyValueArray[0], keyValueArray[1])
    else:
        return (keyValueArray[0], 'stdout')


def _getJobConfigurationsFromArgs(args):
    job = config.Job()
    job.name = 'default'
    for modelFile in args.models:
        model = config.Model()
        model.schema = modelFile
        job.models.append(model)
    templateParameters = _getTemplateParameters(args)

    if args.singleFileTemplates is not None:
        for templateFile in args.singleFileTemplates:
            task = config.Task()
            task.name = templateFile
            task.singleFileTask = config.SingleFileTask()
            (task.singleFileTask.template, task.singleFileTask.destFile) = _splitTemplateAndDestination(templateFile)
            task.singleFileTask.templateParameters = templateParameters
            job.tasks.append(task)

    if args.multiFileTemplates is not None:
        for templateFile in args.multiFileTemplates:
            task = config.Task()
            task.name = templateFile
            task.multiFileTask = config.MultiFileTask()
            (task.multiFileTask.template, task.multiFileTask.destDir) = _splitTemplateAndDestination(templateFile)
            task.multiFileTask.templateParameters = templateParameters
            job.tasks.append(task)
    return [job]


def getJobConfigurations(args):
    """builds an list of code generation Jobs from the given command lines
    and return it
    """

    if args.config is not None:
        return _getJobConfigurationsFromConfigFile(args.config)
    else:
        return _getJobConfigurationsFromArgs(args)


def _foundAllTemplates(codeGenerationJobs):
    """checks up if all template file are accessible. For internal templates the
    template file name is changed

    returns True if all templates are available, else False
    """

    print('\nChecking up templates:')
    foundAll = True
    for job in codeGenerationJobs:
        print('  template for job {}:'.format(job.name))
        for task in job.tasks:
            fileExists = False
            if (task.singleFileTask is not None) and (task.singleFileTask.template is not None):
                (fileExists, task.singleFileTask.template) = _tryToFindTemplate(task.singleFileTask.template)
            elif (task.multiFileTask is not None) and (task.multiFileTask.template is not None):
                (fileExists, task.multiFileTask.template) = _tryToFindTemplate(task.multiFileTask.template)
            if not fileExists:
                foundAll = False
    return foundAll


def _tryToFindTemplate(templateFile):
    """tests if the given file name is a external or an internal template. If it
    is an internal template, then the file name is changed to a relative path.

    Function return a tupel with the true or false as first element, and the file name
    to the found file as second element
    """

    fileExists = False
    templateFileToReturn = templateFile
    if doesFileExist(templateFile):
        fileExists = True
    else:
        internalTemplateName = 'yacg/generators/templates/{}.mako'.format(templateFile)
        fileExists = doesFileExist(internalTemplateName)
        templateFileToReturn = internalTemplateName
    fileExistsString = getOkTxt('found') if fileExists else getErrorTxt('missing')
    print('   {}\t{}'.format(fileExistsString, templateFile))
    return (fileExists, templateFileToReturn)


def _foundAllModels(codeGenerationJobs):
    """checks up if all model file are accessible. For internal templates the
    template file name is changed

    returns True if all templates are available, else False
    """

    print('\nChecking up models:')
    foundAll = True
    for job in codeGenerationJobs:
        print('  Models for job {}:'.format(job.name))
        for model in job.models:
            fileExists = doesFileExist(model.schema)
            fileExistsString = getOkTxt('found') if fileExists \
                else getErrorTxt('missing')
            if not fileExists:
                foundAll = False
            print('   {}\t{}'.format(fileExistsString, model.schema))
    return foundAll


def _isConfigurationValid(codeGenerationJobs):
    """checks up the give job configuration array and
    returns True if valid else if not
    """

    isValid = True
    if (codeGenerationJobs is None) or (len(codeGenerationJobs) == 0):
        errorMsg = getErrorTxt('no generation jobs are given - cancel')
        print(errorMsg)
        return False
    if _foundAllTemplates(codeGenerationJobs) is False:
        isValid = False
    if _foundAllModels(codeGenerationJobs) is False:
        isValid = False
    return isValid


def main():
    """starts the program execution"""
    args = parser.parse_args()
    codeGenerationJobs = getJobConfigurations(args)
    if not _isConfigurationValid(codeGenerationJobs):
        sys.exit(1)
    for job in codeGenerationJobs:
        loadedTypes = readModels(job)
        for task in job.tasks:
            if task.singleFileTask is not None:
                renderSingleFileTemplate(
                    loadedTypes,
                    task.singleFileTask.template,
                    task.singleFileTask.destFile,
                    task.singleFileTask.templateParameters)
                # TODO
            elif task.multiFileTask is not None:
                pass
                # TODO


if __name__ == '__main__':
    main()
