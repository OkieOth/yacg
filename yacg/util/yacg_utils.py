import json
import yaml

from yacg.util.fileUtils import doesFileExist
from yacg.util.outputUtils import printError


def getJobConfigurationsFromConfigFile(configFile):
    if not doesFileExist(configFile):
        printError('\ncan not find config file: {}'.format(configFile))
        return []
    if configFile.endswith('.json'):
        with open(configFile) as config:
            return json.load(config)
    elif configFile.endswith('.yaml') or configFile.endswith('.yaml'):
        with open(configFile) as config:
            return yaml.load(config)
    else:
        printError('\nunknown config file extension, only json or yaml are supportted')
        return []
    # TODO translate dict into object structure
    pass
