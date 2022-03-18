import hashlib
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
    usedFilesDict = {}
    print(">>>>>>>>>>>>>>> {} >>>>>>>>>>>>>>>>".format(modelFile))
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
        #print("file: {}, version: {}, md5: {}".format(trimmedModel, v[0], v[1]))
    print(ret)
    print("<<<<<<<<<<<<<<<<<<<<<<<<<")
