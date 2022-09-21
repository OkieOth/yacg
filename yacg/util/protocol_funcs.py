import hashlib
import json
import logging
import os
import pathlib
from yacg.util.fileUtils import doesFileExist, getDirName
from yacg.model.model import EnumType, ComplexType


def __getMd5FromModelFile(fileName):
    bufferSize = 65536
    md5 = hashlib.md5()

    with open(fileName, 'rb') as f:
        while True:
            data = f.read(bufferSize)
            if not data:
                break
            md5.update(data)
    return md5.hexdigest()


def __trimToLastSlash(commonPart):
    if len(commonPart) == 0:
        return commonPart
    if commonPart[len(commonPart) - 1] != '/':
        lastSlash = commonPart.rfind('/')
        if (lastSlash != 0) and (lastSlash != -1):
            return commonPart[0:lastSlash + 1]
    return commonPart


def doesArrayElemsContainSlashes(strArray):
    for s in strArray:
        if s.find('/') == -1:
            return False
    return True


def scanForIdenticalModelParts(strArray):
    if len(strArray) == 0:
        return ''
    if len(strArray) < 2:
        return __trimToLastSlash(strArray[0])
    if not doesArrayElemsContainSlashes(strArray):
        return ''
    commonPart = ''
    currentPos = 0
    while True:
        if len(strArray[0]) == currentPos:
            return __trimToLastSlash(commonPart)
        s = strArray[0]
        t = s[currentPos:currentPos + 1]
        currentPart = "{}{}".format(commonPart, t)
        lenCurrentPart = len(currentPart)
        isEqual = True
        for str in strArray[1:]:
            if (len(str) < lenCurrentPart) or (not str.startswith(currentPart)):
                isEqual = False
                break
        if not isEqual:
            return __trimToLastSlash(commonPart)
        else:
            commonPart = currentPart
            currentPos = currentPos + 1
    return ''


def getModelMetaData(alloadedTypes, modelFile):
    """check the involved model schemas for md5 sums and the
    contained version

    returns a dictionary that contains a short path form the model as key and
    a dictionary with a 'version' and a 'md5' entry
    """

    usedFilesDict = {}
    for type in alloadedTypes:
        if isinstance(type, EnumType) or isinstance(type, ComplexType):
            if type.source is not None:
                if type.source not in usedFilesDict.keys():
                    md5Sum = __getMd5FromModelFile(type.source)
                    usedFilesDict[type.source] = [type.version, md5Sum]
    identicalPart = scanForIdenticalModelParts(list(usedFilesDict.keys()))
    trimLen = len(identicalPart)
    ret = {}
    for k in usedFilesDict.keys():
        trimmedModel = k[trimLen:]
        v = usedFilesDict[k]
        ret[trimmedModel] = {"version": v[0], "md5": v[1]}
    return ret


def writeProtocolFile(protocolFile, codeGenMetaData):
    if protocolFile is not None:
        dirName = getDirName(protocolFile)
        if not os.path.exists(dirName):
            pathlib.Path(dirName).mkdir(parents=True, exist_ok=True)
        with open(protocolFile, 'w') as outfile:
            json.dump(codeGenMetaData, outfile, indent=4)


def getPreviousMetaData(protocolFile, noLogs):
    if protocolFile is None:
        return {}
    if doesFileExist(protocolFile):
        with open(protocolFile) as input:
            return json.load(input)
    else:
        if not noLogs:
            logging.info('No protocol file found, skip import: {}'.format(protocolFile))
        return {}


def shouldSkipCodeGen(
        skipCodeGenIfVersionUnchanged,
        skipCodeGenIfMd5Unchanged,
        previousJobsMetaData,
        modelMetaData,
        jobName,
        noLogs):
    if (previousJobsMetaData is None) or (modelMetaData is None):
        return False
    if skipCodeGenIfVersionUnchanged or skipCodeGenIfMd5Unchanged:
        previousJobMetaData = previousJobsMetaData.get(jobName, {})
        skip = True
        for k in modelMetaData.keys():
            currentModelMeta = modelMetaData.get(k, None)
            previousModelMeta = previousJobMetaData.get(k, None)
            if (currentModelMeta is not None) and (previousModelMeta is not None):
                if skipCodeGenIfVersionUnchanged:
                    currentVersion = currentModelMeta.get("version", "1")
                    previousVersion = previousModelMeta.get("version", "0")
                    if currentVersion != previousVersion:
                        if not noLogs:
                            logging.info("NEED TO RENDER - version difference: {}, last: {}, current: {}".format(k, previousVersion, currentVersion))  # noqa: E501
                        skip = False
                        break
                elif skipCodeGenIfMd5Unchanged:
                    currentMd5 = currentModelMeta.get("md5", "1")
                    previousMd5 = previousModelMeta.get("md5", "0")
                    if currentMd5 != previousMd5:
                        if not noLogs:
                            logging.info("NEED TO RENDER - md5 difference: {}, last: {}, current: {}".format(k, previousMd5, currentMd5))  # noqa: E501
                        skip = False
                        break
            else:
                if not noLogs:
                    logging.info("NEED TO RENDER - new model: {}".format(k))
                skip = False
                break
        return skip
    else:
        return False
