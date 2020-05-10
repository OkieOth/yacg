import yacg.model.config as config
import yacg.model.modelFuncs as modelFuncs


def trimModelTypes(modelTypes, blackList, whiteList):
    if (blackList is not None) and (len(blackList)>1):
        return _trimModelTypesWithBlackList(modelTypes, blackList)
    elif (whiteList is not None) and (len(whiteList)>1):
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
            _skipTypeIfTypeNameMatch(modelTypes, trimModelTypes, blackListedText)
        elif blackListEntry.type is config.BlackWhiteListEntryTypeEnum.DOMAIN:
            _skipTypeIfDomainNameMatch(modelTypes, trimModelTypes, blackListedText)
        elif blackListEntry.type is config.BlackWhiteListEntryTypeEnum.NOTCONTAINEDATTRIB:
            _addTypeIfAttribNameIsContained(modelTypes, trimModelTypes, blackListedText)
        elif blackListEntry.type is config.BlackWhiteListEntryTypeEnum.CONTAINEDATTRIB:
            _skipTypeIfAttribNameIsContained(modelTypes, trimModelTypes, blackListedText)
        elif blackListEntry.type is config.BlackWhiteListEntryTypeEnum.TAG:
            _skipTypeIfTagNameMatch(modelTypes, trimModelTypes, blackListedText)
        elif blackListEntry.type is config.BlackWhiteListEntryTypeEnum.TYPE:
            _skipTypeIfTypeNameMatch(modelTypes, trimModelTypes, blackListedText)
        else:
            _skipTypeIfTypeNameMatch(modelTypes, trimModelTypes, blackListedText)
    return trimmedModelTypes


def _trimModelTypesWithWhiteList(modelTypes, whiteList):
    trimmedModelTypes = []
    for whiteListEntry in whiteList:
        whiteListedText = whiteListEntry.name
        if whiteListedText is None:
            continue
        if whiteListEntry.type is None:
            _addTypeIfTypeNameMatch(modelTypes, trimModelTypes, whiteListedText)
        elif whiteListEntry.type is config.BlackWhiteListEntryTypeEnum.DOMAIN:
            _addTypeIfDomainNameMatch(modelTypes, trimModelTypes, whiteListedText)
        elif whiteListEntry.type is config.BlackWhiteListEntryTypeEnum.NOTCONTAINEDATTRIB:
            _skipTypeIfAttribNameIsContained(modelTypes, trimModelTypes, whiteListedText)
        elif whiteListEntry.type is config.BlackWhiteListEntryTypeEnum.CONTAINEDATTRIB:
            _addTypeIfAttribNameIsContained(modelTypes, trimModelTypes, whiteListedText)
        elif whiteListEntry.type is config.BlackWhiteListEntryTypeEnum.TAG:
            _addTypeIfTagNameMatch(modelTypes, trimModelTypes, whiteListedText)
        elif whiteListEntry.type is config.BlackWhiteListEntryTypeEnum.TYPE:
            _addTypeIfTypeNameMatch(modelTypes, trimModelTypes, whiteListedText)
        else:
            _skipTypeIfTypeNameMatch(modelTypes, trimModelTypes, whiteListedText)
    return trimmedModelTypes


def _skipTypeIfTypeNameMatch(modelTypes, trimmedModelTypes, textToTest):
    for type in modelTypes:
        if (type.name is not None) and (type.name == textToTest):
            continue
        trimModelTypes.append(type)


def _addTypeIfTypeNameMatch(modelTypes, trimmedModelTypes, textToTest):
    for type in modelTypes:
        if (type.name is not None) and (type.name == textToTest):
            trimModelTypes.append(type)


def _skipTypeIfDomainNameMatch(modelTypes, trimModelTypes, textToTest):
    for type in modelTypes:
        if (hasattr(type, 'domain')) and (textToTest == type.domain):
            continue
        trimModelTypes.append(type)


def _addTypeIfDomainNameMatch(modelTypes, trimModelTypes, textToTest):
    for type in modelTypes:
        if (hasattr(type, 'domain')) and (textToTest == type.domain):
            trimModelTypes.append(type)


def _addTypeIfAttribNameIsContained(modelTypes, trimModelTypes, textToTest):
    for type in modelTypes:
        if modelFuncs.hasProperty(textToTest, type):
            trimModelTypes.append(type)


def _skipTypeIfAttribNameIsContained(modelTypes, trimModelTypes, textToTest):
    for type in modelTypes:
        if modelFuncs.hasProperty(textToTest, type):
            continue
        trimModelTypes.append(type)


def _skipTypeIfTagNameMatch(modelTypes, trimModelTypes, textToTest):
    for type in modelTypes:
        if modelFuncs.hasTag(textToTest, type):
            continue
        trimModelTypes.append(type)


def _addTypeIfTagNameMatch(modelTypes, trimModelTypes, textToTest):
    for type in modelTypes:
        if modelFuncs.hasTag(textToTest, type):
            trimModelTypes.append(type)
