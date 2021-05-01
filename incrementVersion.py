import argparse
import sys
import logging
import json
import semver
import shutil
import yacg.builder.impl.dictionaryBuilder as builder
from yacg.util.fileUtils import doesFileExist
from yacg.util.outputUtils import printError, printInfo

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
    parsedSchema = builder.getParsedSchemaFromJson(args.model)
    currentVersion = parsedSchema.get("version", None)
    if currentVersion is None:
        printInfo('\nModel file does not contain a version: {}'.format(args.model))
        sys.exit(0)
    if not _checkValidVersion(currentVersion):
        printError('\nCurrent version is no valid semver: {}'.format(currentVersion))
        sys.exit(1)
    newVersion = _calcNewVersion(currentVersion, args.version)
    _printOutput(args, newVersion, parsedSchema)


def _printOutput(args, newVersion, parsedSchema):
    if args.dryRun:
        print('model: {}, new version: {}, old version: {}'.format(args.model, newVersion, currentVersion))
    else:
        parsedSchema["version"] = newVersion
        if args.backupExt is not None:
            backupToWrite = '{}.{}'.format(args.model, args.backupExt)
            shutil.copyfile(args.model, backupToWrite)
        with open(args.model, 'w') as outfile:
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


def _calcNewVersion(currentVersion, desiredVersion):
    currentSemVer = semver.VersionInfo.parse(currentVersion)
    if desiredVersion == 'major':
        return str(currentSemVer.bump_major())
    elif desiredVersion == 'minor':
        return str(currentSemVer.bump_minor())
    elif desiredVersion == 'patch':
        return str(currentSemVer.bump_patch())
    else:
        return desiredVersion


if __name__ == '__main__':
    main()
