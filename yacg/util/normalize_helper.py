import json
import yaml
import sys
import yacg.model.modelFuncs as modelFuncs
from yacg.util.outputUtils import printError


def normalizeSchema(schemaAsDict, extractedTypes, sourceFile, outputFile):
    references = []
    modelFuncs.getExternalRefStringsFromDict(schemaAsDict, references)
    refHelperDict = modelFuncs.initReferenceHelperDict(references, sourceFile)
    modelFuncs.initTypesInReferenceHelperDict(refHelperDict, extractedTypes)

    localTypePrefix = modelFuncs.getLocalTypePrefix(schemaAsDict)
    if localTypePrefix is None:
        printError('\nCould not decide if we have here definitions or components/schemas style ... cancel')
        sys.exit(1)
    _replaceRefToLocalVersion(schemaAsDict, refHelperDict, localTypePrefix)
    _addExternalReferencedTypesAndDeps(schemaAsDict, refHelperDict, localTypePrefix)
    _printOutput(outputFile, schemaAsDict)


def _addExternalReferencedTypesAndDeps(schemaAsDict, refHelperDict, localTypePrefix):
    dictToAppendTypes = None
    if localTypePrefix == "#/definitions/":
        definitionsDict = schemaAsDict.get("definitions", None)
        if definitionsDict is None:
            definitionsDict = {}
            schemaAsDict["definitions"] = definitionsDict
        dictToAppendTypes = definitionsDict
    elif localTypePrefix == "#/components/schemas/":
        componentsDict = schemaAsDict.get("components", None)
        if componentsDict is None:
            componentsDict = {}
            schemaAsDict["components"] = componentsDict
        schemaDict = componentsDict.get("schemas", None)
        if schemaDict is None:
            schemaDict = {}
            componentsDict["schemas"] = schemaDict
        dictToAppendTypes = schemaDict

    for _, refHelper in refHelperDict.items():
        relatedTypesList = modelFuncs.getTypeAndAllChildTypes(refHelper.type)
        for t in relatedTypesList:
            if t.name not in dictToAppendTypes.keys():
                dictToAppendTypes[t.name] = modelFuncs.typeToJSONDict(t, localTypePrefix)


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
                    # originDict[key] = 'TODO_NEEDS_TO_BE_REPLACED: {}; {}'.format(localRef, value)
                    originDict[key] = localRef
    pass


def _printOutput(outputFile, schemaAsDict):
    if outputFile is None:
        json.dump(schemaAsDict, sys.stdout, indent=4)
    elif (outputFile.endswith('.yaml')) or (outputFile.endswith('.yml')):
        with open(outputFile, 'w') as outfile:
            yaml.dump(schemaAsDict, outfile, indent=4, sort_keys=False)
    else:
        with open(outputFile, 'w') as outfile:
            json.dump(schemaAsDict, outfile, indent=4)
