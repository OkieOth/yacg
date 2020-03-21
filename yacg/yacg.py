import argparse
import sys
import logging
import util.fileUtils
from util.outputUtils import printError, printOk, printInfo, getErrorTxt, getOkTxt
from builder.jsonBuilder import getModelFromJson 
from builder.yamlBuilder import getModelFromYaml 
from generators.test import renderTemplate

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
parser.add_argument('--template', nargs='+', help='template to process')
parser.add_argument_group('output')
parser.add_argument('--outputDir',  help='dir to write the output')


def getFileExt(fileName):
    """returns the fileextension of a given file name"""

    lastDot = fileName.rindex('.')
    return fileName[lastDot:]

def checkModelsToLoad(args):
    """test if the desired model files exist"""
    
    if not args.model:
        print ('no models given, cancel')
        return False
    print ('\nModels to load:')
    foundAll = True
    for model in args.model:
        modelExists = util.fileUtils.doesFileExist(model)        
        modelExistsString = getOkTxt('yes') if modelExists else getErrorTxt('no') 
        if not modelExists:
            foundAll = False
        print (' {}\t{}'.format(modelExistsString,model))
    return foundAll

def readModels(args):
    """reads all desired models and build the model object tree from it"""

    yamlExtensions = set(['.yaml','.yml'])
    for model in args.model:
        fileExt = getFileExt(model)
        if fileExt.lower() in yamlExtensions:
            getModelFromYaml(model)
            # TODO
        else:
            getModelFromJson(model) 
            # TODO

def main():
    """starts the program execution"""
    args = parser.parse_args()
    argumentsAreOk = True
    if not checkModelsToLoad(args):
        argumentsAreOk = False
    if not argumentsAreOk:
        printError('\nfound errors in configuration, cancel execution')
        sys.exit(1)
    readModels(args)    
    #renderTemplate()

if __name__ == '__main__':
    main()

