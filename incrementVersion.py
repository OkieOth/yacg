import argparse
import os
import sys
import logging
import json
import semver
import shutil
import yacg.builder.impl.dictionaryBuilder as builder
from yacg.util.fileUtils import doesFileExist
from yacg.util.outputUtils import printError, printInfo
from yacg.model.model import ComplexType

description = """Increment the version of a JSON schema file. In addition
it can increment the version of schemas that reference the file with the
incremented version
"""

logging.basicConfig(level=logging.INFO)

parser = argparse.ArgumentParser(prog='incrementVersion', description=description)
parser.add_argument('--model', required=True, help='model schema to update the version')
parser.add_argument('--version', required=True, help='new version [sem ver|major|minor|patch]')
parser.add_argument('--backupExt', help='extension for backups of the original files')
parser.add_argument('--dirToCheckForRefs', help='directory to check for references in json schemas')
parser.add_argument('--dryRun', help='if set, then no file is changed', action='store_true')


class SemVerDummy:
    def __init__(self, version):
        self.version = version


def main():
    args = parser.parse_args()
    if not doesFileExist(args.model):
        printError('\nModel file not found ... cancel: {}'.format(args.model))
        sys.exit(1)
    if not _checkValidVersion(args.version):
        printError('\nNo valid version argument was given, check the help: {}'.format(args.version))
        sys.exit(1)
    if not _checkDirToCheckForRefs(args.dirToCheckForRefs):
        printError("\nThe given directory to check for references isn't a valid dir: {}".format(args.dirToCheckForRefs))
        sys.exit(1)
    parsedSchema = builder.getParsedSchemaFromJson(args.model)
    currentVersion = parsedSchema.get("version", None)
    if currentVersion is None:
        printInfo('\nModel file does not contain a version: {}'.format(args.model))
        sys.exit(0)
    if not _checkValidVersion(currentVersion):
        printError('\nCurrent version is no valid semver: {}'.format(currentVersion))
        sys.exit(1)
    newVersion = _calcNewVersion(currentVersion, args.version, True)
    logging.info("modelFile: {}, currentVersion: {}, newVersion: {}".format(args.model, currentVersion, newVersion))
    _printOutput(args.model, args.backupExt, args.dryRun, newVersion, parsedSchema, currentVersion)
    if args.dirToCheckForRefs is not None:
        filesToCheckList = _getJsonSchemaFileNames(args.dirToCheckForRefs)
        _checkForReferences(args, newVersion, args.model, filesToCheckList, [args.model])


def _checkDirToCheckForRefs(dirToCheckForRefs):
    if dirToCheckForRefs is None:
        return True
    return os.path.isdir(dirToCheckForRefs)


def _getJsonSchemaFileNames(dirToCheckForRefs):
    foundJsonFiles = []
    for root, dirs, files in os.walk(dirToCheckForRefs):
        for file in files:
            if file.endswith('.json'):
                foundJsonFiles.append(root + '/' + file)
    return foundJsonFiles


def _checkForReferences(args, newVersion, modelFile, filesToCheckList, alreadyCheckedList):
    """This function search for all json files in the configured dirToCheckForRefs.
    In the found json files it looks for references to the originally changed model file
    and increments there the version. The following rules are processed:
    1. If the new version was given by [major, minor, patch], then the version of the
        referencing files is incremented in the same way.
    2. If the new version was given as semver, then the major version of referencing
        files is incremented

    Keyword arguments:
    args -- command line arguments
    newVersion -- version that was set for the first model in the command
    modelFile -- model files that could be referenced
    filesToCheckList -- list of files that have to be tests for references
    alreadyCheckedList -- list with all files that are already checked ... to avoid circular dependencies
    """

    newModelsToCheck = []
    for file in filesToCheckList:
        if file in alreadyCheckedList:
            continue
        parsedSchema = builder.getParsedSchemaFromJson(file)
        # search form modelFileReference
        if not isinstance(parsedSchema, dict):
            continue
        currentVersion = parsedSchema.get("version", None)
        if currentVersion is None:
            continue
        logging.info("checking {} for references ...".format(file))
        if _hasModelReference(parsedSchema, file, modelFile):
            logging.info("      ... found")
            newVersion = _calcNewVersion(currentVersion, args.version, False)
            _printOutput(file, args.backupExt, args.dryRun, newVersion, parsedSchema, currentVersion)
            if file not in newModelsToCheck:
                newModelsToCheck.append(file)
            alreadyCheckedList.append(file)
    for model in newModelsToCheck:
        _checkForReferences(args, newVersion, model, filesToCheckList, alreadyCheckedList)


def _hasModelReference(parsedSchema, parsedFile, modelFile):
    """Check if the parsedSchema dict contains a reference to the modelFile. If a reference existss
    the True is returned

    Keyword arguments:
    parsedSchema -- dictionary from the current parsed JSON file
    modelFile -- file name of another schema to look for by reference
    """

    parsedFilePath = os.path.abspath(parsedFile)
    modelFilePath = os.path.abspath(modelFile)
    parsedTypeList = builder.extractTypes(parsedSchema, parsedFilePath, [], True)
    for t in parsedTypeList:
        if isinstance(t, ComplexType):
            if modelFilePath == t.source:
                return True
    return False


def _printOutput(modelFile, backupExt, dryRun, newVersion, parsedSchema, currentVersion):
    if dryRun:
        print('model: {}, new version: {}, old version: {}'.format(modelFile, newVersion, currentVersion))
    else:
        parsedSchema["version"] = newVersion
        if backupExt is not None:
            backupToWrite = '{}.{}'.format(modelFile, backupExt)
            logging.info("write modelFile backup: {}".format(backupToWrite))
            shutil.copyfile(modelFile, backupToWrite)
        logging.info("write modelFile with updated version: {}".format(modelFile))
        with open(modelFile, 'w') as outfile:
            json.dump(parsedSchema, outfile, indent=4)


def _checkValidVersion(versionStr):
    if versionStr == 'major':
        return True
    elif versionStr == 'minor':
        return True
    elif versionStr == 'patch':
        return True
    else:
        # check for semver ... strange syntax by cmd_check function
        dummy = SemVerDummy(versionStr)
        try:
            semver.cmd_check(dummy)
            return True
        except ValueError:
            return False


def _calcNewVersion(currentVersion, desiredVersion, keepDesiredVersionInsteadOfBumpingMajor):
    currentSemVer = semver.VersionInfo.parse(currentVersion)
    if desiredVersion == 'major':
        return str(currentSemVer.bump_major())
    elif desiredVersion == 'minor':
        return str(currentSemVer.bump_minor())
    elif desiredVersion == 'patch':
        return str(currentSemVer.bump_patch())
    elif keepDesiredVersionInsteadOfBumpingMajor:
        return desiredVersion
    else:
        # in case of we handling a referencing file instead of the initial updated model
        return str(currentSemVer.bump_major())


if __name__ == '__main__':
    main()
