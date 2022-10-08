import argparse
import sys
import json
import yaml
import logging
from yacg.util.fileUtils import doesFileExist
from yacg.util.outputUtils import printError
import yacg.builder.impl.dictionaryBuilder as builder
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
    extractedTypes = builder.extractTypes(schemaAsDict, sourceFile, [], True)
    references = []
    modelFuncs.getExternalRefStringsFromDict(schemaAsDict, references)
    refHelperDict = modelFuncs.initReferenceHelperDict(references, sourceFile)
    modelFuncs.initTypesInReferenceHelperDict(refHelperDict, extractedTypes)

    localTypePrefix = modelFuncs.getLocalTypePrefix(schemaAsDict)
    if localTypePrefix is None:
        printError('\nCould not decide if we have here definitions or components/schema style ... cancel')
        sys.exit(1)
    _replaceRefToLocalVersion(schemaAsDict, refHelperDict, localTypePrefix)
    _addExternalReferencedTypesAndDeps(schemaAsDict, refHelperDict)
    _printOutput(args, schemaAsDict)


def _addExternalReferencedTypesAndDeps(schemaAsDict, refHelperDict):
    schemaDefinitions = schemaAsDict.get('definitions', None)
    dictToAppendTypes = None
    if schemaDefinitions is not None:
        dictToAppendTypes = schemaDefinitions
    else:
        componentsDict = schemaAsDict.get('components', None)
        if componentsDict is not None:
            dictToAppendTypes = componentsDict
    for _, refHelper in refHelperDict:
        relatedTypesList = modelFuncs.getTypeAndAllChildTypes(refHelper.type)
        for t in relatedTypesList:
            if t.name not in dictToAppendTypes.keys():
                dictToAppendTypes[t.name] = modelFuncs.typeToJSONDict(t)


def _replaceRefToLocalVersionFromList(value, refHelperDict, localTypePrefix):
    newList = []
    for elem in value:
        if isinstance(elem, dict):
            _replaceRefToLocalVersion(elem, refHelperDict, localTypePrefix)
            newList.append(elem)
        if isinstance(elem, list):
            newList.append(_replaceRefToLocalVersionFromList(value, refHelperDict, localTypePrefix))
    return newList


def _replaceRefToLocalVersion(schemaDict, refHelperDict, localTypePrefix):
    for key in schemaDict.keys():
        value = schemaDict.get(key)
        if isinstance(value, dict):
            _replaceRefToLocalVersion(value, refHelperDict, localTypePrefix)
        if isinstance(value, list):
            newList = _replaceRefToLocalVersionFromList(value, refHelperDict, localTypePrefix)
            schemaDict[key] = newList
        else:
            _testForExternalRefAndReplace(key, value, schemaDict, refHelperDict, localTypePrefix)


def _testForExternalRefAndReplace(key, value, originDict, refHelperDict, localTypePrefix):
    if (key == '$ref') and isinstance(value, str):
        lowerValue = value.lower()
        externalRef = (lowerValue.find('.json') != -1) or (lowerValue.find('.yaml') != -1) or (lowerValue.find('.yml') != -1)
        if externalRef:
            for k, v in refHelperDict.items():
                if k == value:
                    localRef = localTypePrefix + v.typeName
                    #originDict[key] = 'TODO_NEEDS_TO_BE_REPLACED: {}; {}'.format(localRef, value)
                    originDict[key] = localRef
    pass


def _printOutput(args, schemaAsDict):
    if args.outputFile is None:
        json.dump(schemaAsDict, sys.stdout, indent=4)
    elif (args.outputFile.endswith('.yaml')) or (args.outputFile.endswith('.yml')):
        with open(args.outputFile, 'w') as outfile:
            yaml.dump(schemaAsDict, outfile, indent=4)
    else:
        with open(args.outputFile, 'w') as outfile:
            json.dump(schemaAsDict, outfile, indent=4)


if __name__ == '__main__':
    main()
