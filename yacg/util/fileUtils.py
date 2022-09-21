import os.path


def doesFileExist(filePathToTest):
    return os.path.isfile(filePathToTest)


def getInternalTemplatePath(relTemplatePathFromProjectRoot):
    currentPath = os.path.realpath(__file__)
    lastSlash = currentPath.rindex('/')
    return currentPath[:lastSlash] + '/../' + relTemplatePathFromProjectRoot


def getDirName(fileName):
    try:
        lastSlash = fileName.rindex('/')
        if lastSlash == 0:
            return ""
        else:
            return fileName[:lastSlash]
    except ValueError:
        return ""