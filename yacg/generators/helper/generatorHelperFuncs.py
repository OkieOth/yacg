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
    for blackListEntry in blackList:
        blackListedText = blackListEntry.name
        if blackListedText is None:
            continue
        if blackListEntry.type is None:
            _skipTypeIfTypeNameMatch(modelTypes, trimmedModelTypes, blackListedText)
        elif blackListEntry.type is config.BlackWhiteListEntryTypeEnum.DOMAIN:
            _skipTypeIfDomainNameMatch(modelTypes, trimmedModelTypes, blackListedText)
        elif blackListEntry.type is config.BlackWhiteListEntryTypeEnum.NOTCONTAINEDATTRIB:
            _addTypeIfAttribNameIsContained(modelTypes, trimmedModelTypes, blackListedText)
        elif blackListEntry.type is config.BlackWhiteListEntryTypeEnum.CONTAINEDATTRIB:
            _skipTypeIfAttribNameIsContained(modelTypes, trimmedModelTypes, blackListedText)
        elif blackListEntry.type is config.BlackWhiteListEntryTypeEnum.TAG:
            _skipTypeIfTagNameMatch(modelTypes, trimmedModelTypes, blackListedText)
        elif blackListEntry.type is config.BlackWhiteListEntryTypeEnum.TYPE:
            _skipTypeIfTypeNameMatch(modelTypes, trimmedModelTypes, blackListedText)
        elif blackListEntry.type is config.BlackWhiteListEntryTypeEnum.TYPETYPE:
            _skipTypeIfTypeTypeMatch(modelTypes, trimmedModelTypes, blackListedText)
        else:
            _skipTypeIfTypeNameMatch(modelTypes, trimmedModelTypes, blackListedText)
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


def _skipTypeIfTypeNameMatch(modelTypes, trimmedModelTypes, textToTest):
    for typeObj in modelTypes:
        if (typeObj.name is not None) and (typeObj.name == textToTest):
            continue
        trimmedModelTypes.append(typeObj)


def _skipTypeIfTypeTypeMatch(modelTypes, trimmedModelTypes, textToTest):
    for typeObj in modelTypes:
        typeTypeStr = type(typeObj).__name__
        if (textToTest is not None) and (typeTypeStr == textToTest):
            continue
        trimmedModelTypes.append(typeObj)


def _addTypeIfTypeNameMatch(modelTypes, trimmedModelTypes, textToTest):
    for typeObj in modelTypes:
        if (typeObj.name is not None) and (typeObj.name == textToTest):
            trimmedModelTypes.append(typeObj)


def _addTypeIfTypeTypeMatch(modelTypes, trimmedModelTypes, textToTest):
    for typeObj in modelTypes:
        typeTypeStr = type(typeObj).__name__
        if (textToTest is not None) and (typeTypeStr == textToTest):
            trimmedModelTypes.append(typeObj)


def _skipTypeIfDomainNameMatch(modelTypes, trimmedModelTypes, textToTest):
    for typeObj in modelTypes:
        if (hasattr(typeObj, 'domain')) and (textToTest == typeObj.domain):
            continue
        trimmedModelTypes.append(typeObj)


def _addTypeIfDomainNameMatch(modelTypes, trimmedModelTypes, textToTest):
    for typeObj in modelTypes:
        if (hasattr(typeObj, 'domain')) and (textToTest == typeObj.domain):
            trimmedModelTypes.append(typeObj)


def _addTypeIfAttribNameIsContained(modelTypes, trimmedModelTypes, textToTest):
    for typeObj in modelTypes:
        if modelFuncs.hasProperty(textToTest, typeObj):
            trimmedModelTypes.append(typeObj)


def _skipTypeIfAttribNameIsContained(modelTypes, trimmedModelTypes, textToTest):
    for typeObj in modelTypes:
        if modelFuncs.hasProperty(textToTest, typeObj):
            continue
        trimmedModelTypes.append(typeObj)


def _skipTypeIfTagNameMatch(modelTypes, trimmedModelTypes, textToTest):
    for typeObj in modelTypes:
        if modelFuncs.hasTag(textToTest, typeObj):
            continue
        trimmedModelTypes.append(typeObj)


def _addTypeIfTagNameMatch(modelTypes, trimmedModelTypes, textToTest):
    for typeObj in modelTypes:
        if modelFuncs.hasTag(textToTest, typeObj):
            trimmedModelTypes.append(typeObj)
