import os.path

def doesFileExist(filePathToTest):
    return os.path.isfile(filePathToTest)

def getInternalTemplatePath(relTemplatePathFromProjectRoot):
    currentPath = os.path.realpath(__file__)
    lastSlash = currentPath.rindex('/')
    return currentPath[:lastSlash] + '/../' + relTemplatePathFromProjectRoot

