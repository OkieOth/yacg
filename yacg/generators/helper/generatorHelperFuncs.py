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
        else:
            _skipTypeIfTypeNameMatch(modelTypes, trimmedModelTypes, whiteListedText)
    return trimmedModelTypes


def _skipTypeIfTypeNameMatch(modelTypes, trimmedModelTypes, textToTest):
    for type in modelTypes:
        if (type.name is not None) and (type.name == textToTest):
            continue
        trimmedModelTypes.append(type)


def _addTypeIfTypeNameMatch(modelTypes, trimmedModelTypes, textToTest):
    for type in modelTypes:
        if (type.name is not None) and (type.name == textToTest):
            trimmedModelTypes.append(type)


def _skipTypeIfDomainNameMatch(modelTypes, trimmedModelTypes, textToTest):
    for type in modelTypes:
        if (hasattr(type, 'domain')) and (textToTest == type.domain):
            continue
        trimmedModelTypes.append(type)


def _addTypeIfDomainNameMatch(modelTypes, trimmedModelTypes, textToTest):
    for type in modelTypes:
        if (hasattr(type, 'domain')) and (textToTest == type.domain):
            trimmedModelTypes.append(type)


def _addTypeIfAttribNameIsContained(modelTypes, trimmedModelTypes, textToTest):
    for type in modelTypes:
        if modelFuncs.hasProperty(textToTest, type):
            trimmedModelTypes.append(type)


def _skipTypeIfAttribNameIsContained(modelTypes, trimmedModelTypes, textToTest):
    for type in modelTypes:
        if modelFuncs.hasProperty(textToTest, type):
            continue
        trimmedModelTypes.append(type)


def _skipTypeIfTagNameMatch(modelTypes, trimmedModelTypes, textToTest):
    for type in modelTypes:
        if modelFuncs.hasTag(textToTest, type):
            continue
        trimmedModelTypes.append(type)


def _addTypeIfTagNameMatch(modelTypes, trimmedModelTypes, textToTest):
    for type in modelTypes:
        if modelFuncs.hasTag(textToTest, type):
            trimmedModelTypes.append(type)
