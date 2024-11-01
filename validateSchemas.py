import argparse
import sys
import json
import yacg.builder.impl.dictionaryBuilder as builder
from yacg.util.outputUtils import printError

description = """Takes a schema or a base directory and tries to load the found schemas for 
validation purposes. The validation isn't done against standards, but the loading capabilities
are used for it.
"""


parser = argparse.ArgumentParser(prog='validate', description=description)
parser.add_argument('--schema', help='path to model schema')
parser.add_argument('--inputDir', help='path to start to search for JSON schemas')
parser.add_argument('--noEmptySchemas', help='Checks that at least one type is found in the schema', action='store_true')  # noqa: E501


def main():
    args = parser.parse_args()
    if (args.schema is None) and (args.inputDir is None):
        printError("\nNeither a schema file nor a inputDir is given, so don't know what to validate")
        sys.exit(1)
    if args.schema is not None:
        try:
            schemaAsDict = builder.getParsedSchemaFromJson(args.schema)
            if args.noEmptySchemas:
                extractedTypes = builder.extractTypes(schemaAsDict, args.schema, [], False)
                if len(extractedTypes) == 0:
                    printError(f"Schema file doesn't contain a type: ${args.schema}")
                    sys.exit(1)            
        except Exception as e:
            printError(f"Error while validating schema: ${args.schema}")
            sys.exit(1)            
    if args.inputDir is not None:
        pass


if __name__ == '__main__':
    main()

