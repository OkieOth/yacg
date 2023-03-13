from http.server import BaseHTTPRequestHandler, HTTPServer
import argparse
import sys
import yaml
import json
import copy
from yacg.util.fileUtils import doesFileExist
import yacg.builder.impl.dictionaryBuilder as builder
import yacg.model.randomFuncs as randomFuncs
from yacg.util.fileUtils import getFileExt
import createRandomData
import customRandomContraints


description = """
Reads a JSON schema model in JSON our YAML and start a simple http server on a given
port. A simple request on that port with `/{TYPENAME}` will return random data
of that type.
"""

parser = argparse.ArgumentParser(prog='createRandomData', description=description)
parser.add_argument('--model', help='with random generation information annotated model schema')
parser.add_argument('--host', help='host to bind the server on, default localhost')
parser.add_argument('--port', help='host to bind the server on, default 8080')
parser.add_argument('--type', nargs='+', help='type name to generate data for, alternative to specific annotation')
parser.add_argument('--yaml', help='the default output is JSON, set this if YAML output desired', action='store_true')
parser.add_argument('--noIndent', help='set this if the output should not be beautified', action='store_true')
parser.add_argument('--defaultElemCount', help='default number of elements to generate for a type')
parser.add_argument('--defaultTypeDepth', help='default depth to generate complex types')
parser.add_argument('--defaultMinArrayElemCount', help='default minimal array element count')
parser.add_argument('--defaultMaxArrayElemCount', help='default maximal array element count')
parser.add_argument('--defaultMinDate', help='default minimal date for date and timestamp fields')
parser.add_argument('--defaultMaxDate', help='default maximal date for date and timestamp fields')


defaultHostName = "localhost"
defaultServerPort = 8080

initialDefaultConfig = None

loadedTypes = []


def _extractParameters(pathAndParameters):
    parameters = {}
    if len(pathAndParameters) > 1:
        for p in pathAndParameters[1].split("&"):
            keyAndValue = p.split("=")
            if len(keyAndValue) == 2:
                parameters[keyAndValue[0]] = keyAndValue[1]
    return parameters


def __createDefaultConfig(parameters):
    global initialDefaultConfig
    defaultConfig = copy.copy(initialDefaultConfig)
    count = parameters.get("count", None)
    if count is not None:
        defaultConfig.defaultElemCount = int(count)

    typeDepth = parameters.get("typeDepth", None)
    if typeDepth is not None:
        defaultConfig.defaultTypeDepth = int(typeDepth)

    minArrayElemCount = parameters.get("minArrayElemCount", None)
    if minArrayElemCount is not None:
        defaultConfig.defaultMinArrayElemCount = int(minArrayElemCount)

    maxArrayElemCount = parameters.get("maxArrayElemCount", None)
    if maxArrayElemCount is not None:
        defaultConfig.defaultMaxArrayElemCount = int(maxArrayElemCount)

    minDate = parameters.get("minDate", None)
    if minDate is not None:
        defaultConfig.defaultMinDate = minDate

    maxDate = parameters.get("maxDate", None)
    if maxDate is not None:
        defaultConfig.defaultMaxDate = maxDate

    probabilityToBeEmpty = parameters.get("probabilityToBeEmpty", None)
    if probabilityToBeEmpty is not None:
        defaultConfig.defaultProbabilityToBeEmpty = int(probabilityToBeEmpty)

    return defaultConfig


def _getJson(randomDataDict, noIndent):
    if noIndent:
        return json.dumps(randomDataDict)
    else:
        return json.dumps(randomDataDict, indent=4)


def _getYaml(randomDataDict, noIndent):
    if noIndent:
        return yaml.dumps(randomDataDict, sort_keys=False)
    else:
        return yaml.dumps(randomDataDict, indent=4, sort_keys=False)


def _getRandomContent(parameters, currentPath):
    global loadedTypes
    defaultConfig = __createDefaultConfig(parameters)
    if defaultConfig.defaultElemCount is None:
        defaultConfig.defaultElemCount = 1
    for t in loadedTypes:
        if (t.name is not None) and ( t.name.lower() == currentPath):
            randomData = randomFuncs.generateRandomData(t, defaultConfig)
            shouldUse, value = customRandomContraints.doPostProcessing(t.name, randomData)
            if not shouldUse:
                continue
            noIndent = False
            if parameters.get("noIndent", None) is not None:
                noIndent = True
            if parameters.get("yaml", None) is not None:
                return _getYaml(randomData, noIndent)
            else:
                return _getJson(randomData, noIndent)
    return None


def _getTypes(parameters):
    global loadedTypes
    ret = []
    for t in loadedTypes:
        ret.append(t.name)
    noIndent = False
    if parameters.get("noIndent", None) is not None:
        noIndent = True
    if parameters.get("yaml", None) is not None:
        return _getYaml(ret, noIndent)
    else:
        return _getJson(ret, noIndent)


class RandomServer(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            pathAndParameters = self.path.split("?")
            currentPath = pathAndParameters[0].lower()
            currentPath = currentPath[1:]
            parameters = _extractParameters(pathAndParameters)
            content = None
            if (len(currentPath) == 0) or ((currentPath == "types") and (parameters.get("all", None) is not None)):
                content = _getTypes(parameters)
            else:
                content = _getRandomContent(parameters, currentPath)
            if content is not None:
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(bytes(content, "utf-8"))
            else:
                self.send_error(404, "type '{}' not found in loaded model".format(pathAndParameters[0]))
        except BaseException as error:
            self.send_error(500, "error while processing request: {}".format(error))


def main(args):
    yamlExtensions = set(['.yaml', '.yml'])
    fileExt = getFileExt(args.model)
    global loadedTypes
    global initialDefaultConfig
    if fileExt.lower() in yamlExtensions:
        dict = builder.getParsedSchemaFromYaml(args.model)
    else:
        dict = builder.getParsedSchemaFromJson(args.model)
    initialDefaultConfig = createRandomData.createDefaultConfig(args)
    loadedTypes = builder.extractTypes(dict, args.model, [], False)
    randomFuncs.extendMetaModelWithRandomConfigTypes(loadedTypes)
    host = defaultHostName if args.host is None else args.host
    port = defaultServerPort if args.port is None else int(args.port)

    webServer = HTTPServer((host, port), RandomServer)
    print("Server started http://%s:%s" % (host, port))
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass
    webServer.server_close()
    print("Server stopped.")


if __name__ == '__main__':
    args = parser.parse_args()
    #if args.model is None:
    #    args.model = "resources/models/json/yacg_config_schema.json"
    if args.model is None:
        print('\nModel file not given. It can be passed as parameter or over stdin ... cancel')
        sys.exit(1)
    if not doesFileExist(args.model):
        print('\nModel file not found ... cancel: {}'.format(args.model))
        sys.exit(1)
    main(args)
