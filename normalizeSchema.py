import argparse
import sys
import logging
from yacg.util.fileUtils import doesFileExist
from yacg.util.outputUtils import printError
import yacg.builder.impl.dictionaryBuilder as builder
import yacg.util.normalize_helper as normalizeHelper
import yacg.model.modelFuncs as modelFuncs


description = """Reads a JSON schema model in JSON our YAML format and includes all external
references into that file
"""

logging.basicConfig(level=logging.INFO)

parser = argparse.ArgumentParser(prog='normalizeSchema', description=description)
parser.add_argument('--model', help='model schema to normalize')
parser.add_argument('--outputFile', help='name of the file to create as output')
parser.add_argument('--json', help='JSON input given', action='store_true')
parser.add_argument('--yaml', help='YAML input given', action='store_true')
parser.add_argument('--definitionsStyle', help="local definitions will aprear under '#/definitions' in the schema", action='store_true')
parser.add_argument('--componentsStyle', help="local definitions will aprear under '#/components/schemas' in the schema", action='store_true')


def main():
    args = parser.parse_args()
    if args.model is None:
        printError('\nModel file not given. It can be passed as parameter or over stdin ... cancel')
        sys.exit(1)
    if not doesFileExist(args.model):
        printError('\nModel file not found ... cancel: {}'.format(args.model))
        sys.exit(1)
    if (not args.json) and (not args.yaml):
        printError('\nEither json or yaml should be given as param ... cancel')
        sys.exit(1)
    sourceFile = args.model
    if args.json:
        # load a new model from a json file
        schemaAsDict = builder.getParsedSchemaFromJson(sourceFile)
    else:
        # load new model from a yaml file
        schemaAsDict = builder.getParsedSchemaFromYaml(sourceFile)
    # find all external referenced types ...
    extractedTypes = builder.extractTypes(schemaAsDict, sourceFile, [], False)
    localTypePrefix = modelFuncs.getLocalTypePrefix(schemaAsDict)
    if localTypePrefix is None:
        if args.definitionsStyle:
            localTypePrefix = "#/definitions/"
        elif args.componentsStyle:
            localTypePrefix = "#/components/schemas/"
        else:
            printError('\nCould not decide if we have here definitions or components/schemas style ... cancel')
            sys.exit(1)

    normalizeHelper.normalizeSchema(schemaAsDict, extractedTypes, sourceFile, args.outputFile, localTypePrefix)


if __name__ == '__main__':
    main()
