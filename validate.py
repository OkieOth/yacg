import argparse
import sys
import json
import yacg.builder.impl.dictionaryBuilder as builder
from yacg.util.outputUtils import printError
from yacg.util.fileUtils import doesFileExist
from jsonspec.validators import load

description = """take a schema and a modelfile and tries to validate it
against the schema.

Attention, draft 07 of JSON schema isn't fully supported.
"""


parser = argparse.ArgumentParser(prog='validate', description=description)
parser.add_argument('--schema', help='path to model schema as validation base')
parser.add_argument('--inputFile', help='path to the json file to validate')
parser.add_argument('--draft07hack', help='remove draft-07 tag from the schema', action='store_true')


def main():
    args = parser.parse_args()
    if args.schema is None:
        printError('\nSchema file not given. It needs to be passed as parameter')
        sys.exit(1)
    if not doesFileExist(args.schema):
        printError('\nSchema file not found ... cancel: {}'.format(args.schema))
        sys.exit(1)
    if args.inputFile is None:
        printError('\nInput file not given. It needs to be passed as parameter')
        sys.exit(1)
    if not doesFileExist(args.inputFile):
        printError('\nInput file not found ... cancel: {}'.format(args.inputFile))
        sys.exit(1)
    schemaAsDict = builder.getParsedSchemaFromJson(args.schema)
    inputAsDict = builder.getParsedSchemaFromJson(args.inputFile)
    if args.draft07hack: 
        schemaVersion = schemaAsDict.get("$schema", None)
        if schemaVersion == "http://json-schema.org/draft-07/schema#":
            del schemaAsDict["$schema"]
    validator = load(schemaAsDict)
    validator.validate(inputAsDict)


if __name__ == '__main__':
    main()

