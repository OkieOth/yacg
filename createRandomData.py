import argparse
import sys
import logging
from yacg.util.fileUtils import doesFileExist
from yacg.util.outputUtils import printError
from yacg.builder.jsonBuilder import getModelFromJson
from yacg.builder.yamlBuilder import getModelFromYaml
import yacg.util.normalize_helper as normalizeHelper
import yacg.model.modelFuncs as modelFuncs
from yacg.util.fileUtils import getFileExt


description = """Reads a JSON schema model in JSON our YAML generates random data
for specific annotated types
"""

logging.basicConfig(level=logging.INFO)

parser = argparse.ArgumentParser(prog='createRandomData', description=description)
parser.add_argument('--model', help='with random generation information annotated model schema')
parser.add_argument('--outputDir', help='name of the directory to store the data with random data')
parser.add_argument('--type', help='type name to generate data for, alternative to specific annotation')
parser.add_argument('--defaultElemCount', help='default number of elements to generate for a type')
parser.add_argument('--defaultTypeDepth', help='default depth to generate complex types')
parser.add_argument('--defaultMinArrayElemCount', help='default minimal array element count')
parser.add_argument('--defaultMaxArrayElemCount', help='default maximal array element count')
parser.add_argument('--defaultMinDate', help='default minimal date for date and timestamp fields')
parser.add_argument('--defaultMaxDate', help='default maximal date for date and timestamp fields')


def _searchForTypesToGenerateAndProcessThem(args, loadedTypes):
    """takes the meta model ..."""

    # TODO
    pass


def main():
    args = parser.parse_args()
    if args.model is None:
        printError('\nModel file not given. It can be passed as parameter or over stdin ... cancel')
        sys.exit(1)
    if not doesFileExist(args.model):
        printError('\nModel file not found ... cancel: {}'.format(args.model))
        sys.exit(1)
    yamlExtensions = set(['.yaml', '.yml'])
    fileExt = getFileExt(args.model)
    loadedTypes = []
    if fileExt.lower() in yamlExtensions:
        loadedTypes = getModelFromYaml(args.model, loadedTypes)
    else:
        loadedTypes = getModelFromJson(args.model, loadedTypes)
    _extendMetaModelWithRandomConfigTypes(args, loadedTypes)
    _searchForTypesToGenerateAndProcessThem(args, loadedTypes)


if __name__ == '__main__':
    main()
