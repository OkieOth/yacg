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
parser.add_argument('--model', nargs='+', help='models to process')
parser.add_argument('--config', nargs='?', help='config file')
parser.add_argument_group('processing')
parser.add_argument('--template', help='template to process')
parser.add_argument_group('output')
parser.add_argument('--output',  help='\'stdout\' or the dir to write the output')


def getFileExt(fileName):
    """returns the fileextension of a given file name"""

    lastDot = fileName.rindex('.')
    return fileName[lastDot:]


def checkModelsToLoad(args):
    """test if the desired model files exist"""

    if not args.model:
        print('no models given, cancel')
        return False
    print('\nAvailable models:')
    foundAll = True
    for model in args.model:
        modelExists = doesFileExist(model)
        modelExistsString = getOkTxt('yes') if modelExists \
            else getErrorTxt('no')
        if not modelExists:
            foundAll = False
        print(' {}\t{}'.format(modelExistsString, model))
    return foundAll


def readModels(args):
    """reads all desired models and build the model object tree from it"""

    loadedTypes = []
    yamlExtensions = set(['.yaml', '.yml'])
    for model in args.model:
        fileExt = getFileExt(model)
        if fileExt.lower() in yamlExtensions:
            loadedTypes = getModelFromYaml(model, loadedTypes)
        else:
            loadedTypes = getModelFromJson(model, loadedTypes)
    return loadedTypes


def main():
    """starts the program execution"""
    args = parser.parse_args()
    argumentsAreOk = True
    if not checkModelsToLoad(args):
        argumentsAreOk = False
    if not argumentsAreOk:
        printError('\nfound errors in configuration, cancel execution')
        sys.exit(1)
    loadedTypes = readModels(args)
    if args.template == 'plantuml':
        templateFile = getInternalTemplatePath('generators/templates/plantUml.mako')
        renderSingleFileTemplate(loadedTypes, templateFile, args)


if __name__ == '__main__':
    main()
