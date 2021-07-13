import argparse
import sys
import os
import json
import logging
import modelToYaml
from yacg.util.fileUtils import doesFileExist
from yacg.util.outputUtils import printError, printInfo
import yacg.builder.impl.dictionaryBuilder as builder


description = """Reads a JSON schema model in yaml format and converts it to a
json file
"""

logging.basicConfig(level=logging.INFO)

parser = argparse.ArgumentParser(prog='modelToJson', description=description)
parser.add_argument('--model', help='model schema to convert to JSON')
parser.add_argument('--stdin', help='reads the model content from stdin', action='store_true')
parser.add_argument('--destDir', help='directory to write the JSON versions')
parser.add_argument('--dryRun', help='if set, then no output file is created', action='store_true')


def _printJson(parsedSchema, model, destDir):
    modelFileNameWithoutExt = modelToYaml.trimModelFileName(model)
    modelFile = "{}/{}.json".format(destDir, modelFileNameWithoutExt)
    printInfo('\nWrite JSON: {}'.format(modelFile))
    with open(modelFile, 'w') as outfile:
        json.dump(parsedSchema, outfile, indent=4)


def convertModel(model, dryRun, destDir):
    parsedSchema = builder.getParsedSchemaFromYaml(model)
    modelToYaml.traverseDictAndReplaceRefExtensions(parsedSchema, False)
    if dryRun:
        print(json.dumps(parsedSchema, indent=4))
    else:
        _printJson(parsedSchema, model, destDir)


def main():
    args = parser.parse_args()
    if not args.stdin:
        if args.model is None:
            printError('\nModel file not given. It can be passed as parameter or over stdin ... cancel')
            sys.exit(1)
        if not doesFileExist(args.model):
            printError('\nModel file not found ... cancel: {}'.format(args.model))
            sys.exit(1)
        model = args.model
    else:
        model = modelToYaml.readStdin()
    if (not args.dryRun) and ((args.destDir is None) or (not os.path.isdir(args.destDir))):
        printError('\nDest dir for yaml output not found ... cancel: {}'.format(args.destDir))
        sys.exit(1)
    convertModel(model, args.dryRun, args.destDir)


if __name__ == '__main__':
    main()
