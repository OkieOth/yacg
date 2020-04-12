import argparse
import sys
import logging


from yacg.util.fileUtils import doesFileExist
from yacg.util.outputUtils import printError, getErrorTxt, getOkTxt
from yacg.builder.jsonBuilder import getModelFromJson
from yacg.builder.yamlBuilder import getModelFromYaml
from yacg.generators.singleFileGenerator import renderSingleFileTemplate
from yacg.util.fileUtils import getInternalTemplatePath

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
parser.add_argument('--templates', nargs='+', help='templates to process')
parser.add_argument_group('output')
parser.add_argument('--output', nargs='+', help='output files or directories in order of the given templates')
parser.add_argument_group('additional')
parser.add_argument('--templateParameters', nargs='+', help='additional parameters passed to the templates')


def getFileExt(fileName):
    """returns the fileextension of a given file name"""

    lastDot = fileName.rindex('.')
    return fileName[lastDot:]


def checkTemplatesToUse(args):
    """test if the required model are there"""

    # extend internal models with the full path
    fixedTemplates = []
    for template in args.templates:
        internalTemplateName = 'yacg/generators/templates/{}.mako'.format(template)
        isInternalTemplate = doesFileExist(internalTemplateName)
        if isInternalTemplate is True:
            fixedTemplates.append(internalTemplateName)
        else:
            fixedTemplates.append(template)

    return _checkFilesToUse(fixedTemplates, 'templates')


def checkModelsToLoad(args):
    """test if the desired model files exist"""

    return _checkFilesToUse(args.models, 'models')


def _checkFilesToUse(fileList, fileType):
    if not fileList:
        print('no {} given, cancel'.format(fileType))
        return False
    print('\n{} to use:'.format(fileType))
    foundAll = True
    for file in fileList:
        fileExists = doesFileExist(file)
        fileExistsString = getOkTxt('found') if fileExists \
            else getErrorTxt('missing')
        if not fileExists:
            foundAll = False
        print(' {}\t{}'.format(fileExistsString, file))
    return foundAll


def readModels(args):
    """reads all desired models and build the model object tree from it"""

    loadedTypes = []
    yamlExtensions = set(['.yaml', '.yml'])
    for model in args.models:
        fileExt = getFileExt(model)
        if fileExt.lower() in yamlExtensions:
            loadedTypes = getModelFromYaml(model, loadedTypes)
        else:
            loadedTypes = getModelFromJson(model, loadedTypes)
    return loadedTypes


def getTemplateParameters(args):
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


def main():
    """starts the program execution"""
    args = parser.parse_args()
    argumentsAreOk = True
    if not checkModelsToLoad(args):
        argumentsAreOk = False
    if not checkTemplatesToUse(args):
        argumentsAreOk = False
    if not argumentsAreOk:
        printError('\nfound errors in configuration, cancel execution')
        sys.exit(1)
    loadedTypes = readModels(args)
    templateParameters = getTemplateParameters(args)
    i = 0
    for template in args.templates:
        internalTemplateName = 'generators/templates/{}.mako'.format(template)
        isInternalTemplate = doesFileExist('yacg/{}'.format(internalTemplateName))
        if isInternalTemplate is True:
            templateFile = getInternalTemplatePath(internalTemplateName)
            output = args.output[i]
            renderSingleFileTemplate(loadedTypes, templateFile, output, templateParameters)
        else:
            printError('template not found: {}'.format(template))
        i = i + 1

if __name__ == '__main__':
    main()
