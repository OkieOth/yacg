import yacg.model.config as config
import yacg.model.modelFuncs as modelFuncs


def trimModelTypes(modelTypes, blackList, whiteList):
    if (blackList is not None) and (len(blackList) > 0):
        return _trimModelTypesWithBlackList(modelTypes, blackList)
    elif (whiteList is not None) and (len(whiteList) > 0):
        return _trimModelTypesWithWhiteList(modelTypes, whiteList)
    else:
        return modelTypes


def _trimModelTypesWithBlackList(modelTypes, blackList):
    trimmedModelTypes = []
    for typeObj in modelTypes:
        trimmedModelTypes.append(typeObj)

    for blackListEntry in blackList:
        blackListedText = blackListEntry.name
        if blackListedText is None:
            continue
        if blackListEntry.type is None:
            _skipTypeIfTypeNameMatch(trimmedModelTypes, blackListedText)
        elif blackListEntry.type is config.BlackWhiteListEntryTypeEnum.DOMAIN:
            _skipTypeIfDomainNameMatch(trimmedModelTypes, blackListedText)
        elif blackListEntry.type is config.BlackWhiteListEntryTypeEnum.NOTCONTAINEDATTRIB:
            _addTypeIfAttribNameIsContained(trimmedModelTypes, blackListedText)
        elif blackListEntry.type is config.BlackWhiteListEntryTypeEnum.CONTAINEDATTRIB:
            _skipTypeIfAttribNameIsContained(trimmedModelTypes, blackListedText)
        elif blackListEntry.type is config.BlackWhiteListEntryTypeEnum.TAG:
            _skipTypeIfTagNameMatch(trimmedModelTypes, blackListedText)
        elif blackListEntry.type is config.BlackWhiteListEntryTypeEnum.TYPE:
            _skipTypeIfTypeNameMatch(trimmedModelTypes, blackListedText)
        elif blackListEntry.type is config.BlackWhiteListEntryTypeEnum.TYPETYPE:
            _skipTypeIfTypeTypeMatch(trimmedModelTypes, blackListedText)
        else:
            _skipTypeIfTypeNameMatch(trimmedModelTypes, blackListedText)
    return trimmedModelTypes


def _trimModelTypesWithWhiteList(modelTypes, whiteList):
    trimmedModelTypes = []
    for whiteListEntry in whiteList:
        whiteListedText = whiteListEntry.name
        if whiteListedText is None:
            continue
        if whiteListEntry.type is None:
            _addTypeIfTypeNameMatch(modelTypes, trimmedModelTypes, whiteListedText)
        elif whiteListEntry.type is config.BlackWhiteListEntryTypeEnum.DOMAIN:
            _addTypeIfDomainNameMatch(modelTypes, trimmedModelTypes, whiteListedText)
        elif whiteListEntry.type is config.BlackWhiteListEntryTypeEnum.NOTCONTAINEDATTRIB:
            _skipTypeIfAttribNameIsContained(modelTypes, trimmedModelTypes, whiteListedText)
        elif whiteListEntry.type is config.BlackWhiteListEntryTypeEnum.CONTAINEDATTRIB:
            _addTypeIfAttribNameIsContained(modelTypes, trimmedModelTypes, whiteListedText)
        elif whiteListEntry.type is config.BlackWhiteListEntryTypeEnum.TAG:
            _addTypeIfTagNameMatch(modelTypes, trimmedModelTypes, whiteListedText)
        elif whiteListEntry.type is config.BlackWhiteListEntryTypeEnum.TYPE:
            _addTypeIfTypeNameMatch(modelTypes, trimmedModelTypes, whiteListedText)
        elif whiteListEntry.type is config.BlackWhiteListEntryTypeEnum.TYPETYPE:
            _addTypeIfTypeTypeMatch(modelTypes, trimmedModelTypes, whiteListedText)
        else:
            _skipTypeIfTypeNameMatch(modelTypes, trimmedModelTypes, whiteListedText)
    return trimmedModelTypes


def _skipTypeIfTypeNameMatch(trimmedModelTypes, textToTest):
    typesToTest = []
    for typeObj in trimmedModelTypes:
        typesToTest.append(typeObj)

    for typeObj in typesToTest:
        if (typeObj.name is not None) and (typeObj.name == textToTest):
            trimmedModelTypes.remove(typeObj)


def _skipTypeIfTypeTypeMatch(trimmedModelTypes, textToTest):
    typesToTest = []
    for typeObj in trimmedModelTypes:
        typesToTest.append(typeObj)

    for typeObj in typesToTest:
        typeTypeStr = type(typeObj).__name__
        if (textToTest is not None) and (typeTypeStr == textToTest):
            trimmedModelTypes.remove(typeObj)


def _addTypeIfTypeNameMatch(modelTypes, trimmedModelTypes, textToTest):
    for typeObj in modelTypes:
        if (typeObj.name is not None) and (typeObj.name == textToTest):
            trimmedModelTypes.append(typeObj)


def _addTypeIfTypeTypeMatch(modelTypes, trimmedModelTypes, textToTest):
    for typeObj in modelTypes:
        typeTypeStr = type(typeObj).__name__
        if (textToTest is not None) and (typeTypeStr == textToTest):
            trimmedModelTypes.append(typeObj)


def _skipTypeIfDomainNameMatch(trimmedModelTypes, textToTest):
    typesToTest = []
    for typeObj in trimmedModelTypes:
        typesToTest.append(typeObj)

    for typeObj in typesToTest:
        if (hasattr(typeObj, 'domain')) and (textToTest == typeObj.domain):
            trimmedModelTypes.remove(typeObj)


def _addTypeIfDomainNameMatch(modelTypes, trimmedModelTypes, textToTest):
    for typeObj in modelTypes:
        if (hasattr(typeObj, 'domain')) and (textToTest == typeObj.domain):
            trimmedModelTypes.append(typeObj)


def _addTypeIfAttribNameIsContained(modelTypes, trimmedModelTypes, textToTest):
    for typeObj in modelTypes:
        if modelFuncs.hasProperty(textToTest, typeObj):
            trimmedModelTypes.append(typeObj)


def _skipTypeIfAttribNameIsContained(trimmedModelTypes, textToTest):
    typesToTest = []
    for typeObj in trimmedModelTypes:
        typesToTest.append(typeObj)

    for typeObj in typesToTest:
        if modelFuncs.hasProperty(textToTest, typeObj):
            trimmedModelTypes.remove(typeObj)


def _skipTypeIfTagNameMatch(trimmedModelTypes, textToTest):
    typesToTest = []
    for typeObj in trimmedModelTypes:
        typesToTest.append(typeObj)

    for typeObj in typesToTest:
        if modelFuncs.hasTag(textToTest, typeObj):
            trimmedModelTypes.remove(typeObj)


def _addTypeIfTagNameMatch(modelTypes, trimmedModelTypes, textToTest):
    for typeObj in modelTypes:
        if modelFuncs.hasTag(textToTest, typeObj):
            trimmedModelTypes.append(typeObj)
