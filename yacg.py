import argparse
import sys
import os
import logging
import tempfile
import requests
import shutil
from datetime import datetime
from yacg.util.fileUtils import doesFileExist
from yacg.util.outputUtils import printError, getErrorTxt, getOkTxt
from yacg.builder.jsonBuilder import getModelFromJson
from yacg.builder.yamlBuilder import getModelFromYaml
from yacg.generators.singleFileGenerator import renderSingleFileTemplate
from yacg.generators.multiFileGenerator import renderMultiFileTemplate
from yacg.model.model import DictionaryType, EnumType, ComplexType, ArrayType
import yacg.util.yacg_utils as yacg_utils
import yacg.model.config as config
import yacg.model.modelFuncs as modelFuncs
import yacg.util.protocol_funcs as protocolFuncs
from yacg.util.fileUtils import getFileExt

description = """Yet another code generation.
Program takes one or more models, a bunch of templates and generates
source code from it
"""

logging.basicConfig(level=logging.INFO)

parser = argparse.ArgumentParser(prog='yacg', description=description)
parser.add_argument_group('input')
parser.add_argument('--models', nargs='+', help='models to process')
parser.add_argument('--config', nargs='?', help='config file')
parser.add_argument('--tasks', nargs='+', help='task names from a config file that should be executed')
parser.add_argument('--jobs', nargs='+', help='job names from a config file that should be executed')
parser.add_argument_group('processing')
parser.add_argument('--singleFileTemplates', nargs='+', help='templates to process that creates one file')
parser.add_argument('--multiFileTemplates', nargs='+', help='templates to process that creates one file per type')
parser.add_argument_group('additional')
parser.add_argument('--templateParameters', nargs='+', help='additional parameters passed to the templates')
parser.add_argument('--blackListed', nargs='+', help='types that should not be handled in the template')
parser.add_argument('--whiteListed', nargs='+', help='types that should be handled in the template')
parser.add_argument('--blackListedDomains', nargs='+', help='domains that should not be handled in the template')
parser.add_argument('--whiteListedDomains', nargs='+', help='domains that should be handled in the template')
parser.add_argument('--vars', nargs='+', help='variables that are passed to the processing')
parser.add_argument('--usedFilesOnly', help='import models but only print the used files to stdout', action='store_true')
parser.add_argument('--flattenInheritance', help='flatten included types so that inheritance', action='store_true')
parser.add_argument('--noLogs', help='do not print logs', action='store_true')
parser.add_argument('--protocolFile', help='where the metadata of the used models for this specifig gen job are stored')
parser.add_argument('--skipCodeGenIfVersionUnchanged', help='when the model versions are unchanged, then the codegen is skipped', action='store_true')  # noqa: E501
parser.add_argument('--skipCodeGenIfMd5Unchanged', help='when the model file md5 is unchanged, then the codegen is skipped', action='store_true')  # noqa: E501
parser.add_argument('--skipCodeGenDryRun', help='prints only the log messages if codegen should be skipped', action='store_true')
parser.add_argument('--failIfTypeNamesNotUnique', help='the code execution fails if there are not unique type names in the loaded type tree', action='store_true')  # noqa: E501
parser.add_argument('--makeMultipleTypeNamesUnique', help='if there are type names multiple times in the list of loaded times, they are changed to be unique', action='store_true')  # noqa: E501
parser.add_argument('--removeDicitonaryTypesFromTopLevel', help='Dictionary types are removed from the loaded types list', action='store_true')  # noqa: E501
parser.add_argument('--removeArrayTypesFromTopLevel', help='Array types are removed from the loaded types list', action='store_true')  # noqa: E501
parser.add_argument('--goOnlyWithTopLevelTypes', help='Only top-level-types from the schema remains in the loaded types list', action='store_true')  # noqa: E501
parser.add_argument('--folder2StoreModels', help='Folder to store models from http sources, this works only if they have no external references')  # noqa: E501
parser.add_argument('--delExistingStoredModels', help='set to false to skip download of http located models if they exist locally', action='store_true')  # noqa: E501
parser.add_argument('--folder2StoreTemplates', help='Folder to store templates from http sources, this works only if they have no references')  # noqa: E501
parser.add_argument('--delExistingStoredTemplates', help='set to false to skip download of http located templates if they exist locally', action='store_true')  # noqa: E501


def readModels(configJob, flattenInheritance):
    """reads all desired models and build the model object tree from it"""

    loadedTypes = []
    yamlExtensions = set(['.yaml', '.yml'])
    for model in configJob.models:
        fileExt = getFileExt(model.schema)
        if fileExt.lower() in yamlExtensions:
            loadedTypes = getModelFromYaml(model, loadedTypes)
        else:
            loadedTypes = getModelFromJson(model, loadedTypes)
    return _postProcessLoadedModels(loadedTypes, flattenInheritance)


def _postProcessLoadedModels(loadedTypes, flattenInheritance):
    if flattenInheritance:
        loadedTypes = modelFuncs.flattenTypes(loadedTypes)
    loadedTypes = modelFuncs.processYacgTags(loadedTypes)
    return loadedTypes


def _getVars(args):
    vars = {}
    if args.vars is not None:
        for v in args.vars:
            keyValueArray = v.split('=')
            if (len(keyValueArray) == 2):
                vars[keyValueArray[0]] = keyValueArray[1]
            else:
                printError('\nvar param with wrong structure found ... skipped: {}'.format(v))
    return vars


def _getTemplateParameters(args):
    """extracts the per command line given template parameters, copies them
    into a dictionary and return this dictonary
    """

    templateParameters = []
    if args.templateParameters is not None:
        for parameter in args.templateParameters:
            keyValueArray = parameter.split('=')
            if (len(keyValueArray) == 2):
                templateParam = config.TemplateParam()
                templateParam.name = keyValueArray[0]
                templateParam.value = keyValueArray[1]
                templateParameters.append(templateParam)
            else:
                printError('\ntemplate param with wrong structure found ... skipped: {}'.format(parameter))
    return templateParameters


def _splitTemplateAndDestination(templateArg):
    keyValueArray = templateArg.split('=')
    if (len(keyValueArray) > 1):
        return (keyValueArray[0], keyValueArray[1])
    else:
        return (keyValueArray[0], 'stdout')


def __getSingleFileTemplates(args, job, templateParameters, blackList, whiteList):
    if args.singleFileTemplates is not None:
        for templateFile in args.singleFileTemplates:
            task = config.Task()
            task.name = templateFile
            task.singleFileTask = config.SingleFileTask()
            (task.singleFileTask.template, task.singleFileTask.destFile) = _splitTemplateAndDestination(templateFile)
            task.singleFileTask.templateParams = templateParameters
            task.blackListed = blackList
            task.whiteListed = whiteList
            job.tasks.append(task)


def __getMultiFileTemplates(args, job, templateParameters, blackList, whiteList):
    if args.multiFileTemplates is not None:
        for templateFile in args.multiFileTemplates:
            task = config.Task()
            task.name = templateFile
            task.multiFileTask = config.MultiFileTask()
            (task.multiFileTask.template, task.multiFileTask.destDir) = _splitTemplateAndDestination(templateFile)
            task.multiFileTask.templateParams = templateParameters
            task.multiFileTask.destFilePrefix = __extractFromTemplateParameters('destFilePrefix', templateParameters)
            task.multiFileTask.destFilePostfix = __extractFromTemplateParameters('destFilePostfix', templateParameters)
            task.multiFileTask.destFileExt = __extractFromTemplateParameters('destFileExt', templateParameters)
            task.blackListed = blackList
            task.whiteListed = whiteList
            job.tasks.append(task)


def __extractFromTemplateParameters(parameterName, templateParameters):
    for param in templateParameters:
        if param.name == parameterName:
            return param.value
    return None


def __blackWhiteListEntries(argsList, blackWhiteListType):
    entryObjList = []
    if argsList is None:
        return []
    for entry in argsList:
        entryObj = config.BlackWhiteListEntry()
        keyValueArray = entry.split('=')
        entryObj.name = keyValueArray[0]
        if (len(keyValueArray) == 2):
            entryObj.type = config.BlackWhiteListEntryTypeEnum.valueForString(keyValueArray[1])
        else:
            entryObj.type = blackWhiteListType
        entryObjList.append(entryObj)
    return entryObjList


def __getBlackWhiteListsFromArgs(args):
    blackList = __blackWhiteListEntries(args.blackListed, config.BlackWhiteListEntryTypeEnum.TYPE)
    whiteList = __blackWhiteListEntries(args.whiteListed, config.BlackWhiteListEntryTypeEnum.TYPE)
    blackListDomains = __blackWhiteListEntries(args.blackListedDomains, config.BlackWhiteListEntryTypeEnum.DOMAIN)
    whiteListDomains = __blackWhiteListEntries(args.whiteListedDomains, config.BlackWhiteListEntryTypeEnum.DOMAIN)
    if len(blackListDomains) > 0:
        blackList.extend(blackListDomains)
    if len(whiteListDomains) > 0:
        whiteList.extend(whiteListDomains)
    return blackList, whiteList


def _getJobConfigurationsFromArgs(args):
    job = config.Job()
    job.name = 'default'
    _putArgModelsToJob(args, job)
    templateParameters = _getTemplateParameters(args)
    blackList, whiteList = __getBlackWhiteListsFromArgs(args)
    __getSingleFileTemplates(args, job, templateParameters, blackList, whiteList)
    __getMultiFileTemplates(args, job, templateParameters, blackList, whiteList)
    return [job]


def _putArgModelsToJob(args, job):
    for modelFile in args.models:
        model = config.Model()
        model.schema = modelFile
        job.models.append(model)


def getJobConfigurations(args):
    """builds an list of code generation Jobs from the given command lines
    and return it
    """

    if args.config is not None:
        templateParameters = _getTemplateParameters(args)
        blackList, whiteList = __getBlackWhiteListsFromArgs(args)
        tasksToInclude = args.tasks if args.tasks is not None else []
        jobsToInclude = args.jobs if args.jobs is not None else []
        vars = _getVars(args)
        jobArray = yacg_utils.getJobConfigurationsFromConfigFile(args.config, vars, jobsToInclude, tasksToInclude)
        if (args.models is not None) and (len(args.models) > 0):
            # there are models from the commandline that have to be mixed in the config file data
            for job in jobArray:
                _putArgModelsToJob(args, job)
        if len(templateParameters) == 0:
            return jobArray
        # mix in of command line parameters to increase flexibility
        for job in jobArray:
            for task in job.tasks:
                task.blackListed = blackList
                task.whiteListed = whiteList
                if task.singleFileTask is not None:
                    task.singleFileTask.templateParams = task.singleFileTask.templateParams + templateParameters
                elif task.multiFileTask is not None:
                    task.multiFileTask.templateParams = task.multiFileTask.templateParams + templateParameters
                elif task.randomDataTask is not None:
                    task.randomDataTask.templateParams = task.randomDataTask.templateParams + templateParameters
        return jobArray
    else:
        return _getJobConfigurationsFromArgs(args)


def _foundAllTemplates(codeGenerationJobs, args):
    """checks up if all template file are accessible. For internal templates the
    template file name is changed

    returns True if all templates are available, else False
    """

    logging.info('Checking up templates ...')
    foundAll = True
    for job in codeGenerationJobs:
        logging.info('  template for job {}:'.format(job.name))
        for task in job.tasks:
            fileExists = False
            if (task.singleFileTask is not None) and (task.singleFileTask.template is not None):
                (fileExists, task.singleFileTask.template) = _tryToFindTemplate(task.singleFileTask.template, args)
            elif (task.multiFileTask is not None) and (task.multiFileTask.template is not None):
                (fileExists, task.multiFileTask.template) = _tryToFindTemplate(task.multiFileTask.template, args)
            elif (task.randomDataTask is not None):
                fileExists = True
            if not fileExists:
                foundAll = False
    return foundAll


def _getFileFromRemoteSource(remoteFile, folderToStore, delExistingFiles):
    """downloads a given files from a remote sources and stores it in a given folder. If the given folder does not
    exist, then it is created.

    The function returns a tupel of a boolean, that indicates that the downloaded file now exists, and
    the path of the file that was downloaded.

    Keyword arguments:
    remoteFile -- File to download
    folderToStore - folder to store the downloaded files
    delExistingFile - if true, then a file with the same name will be deleted before the download. 
    """

    try:
        # e.g. https:**/**/bla.com/xx
        i = remoteFile.find("/")
        # e.g. https:/**/**bla.com/xx
        i = remoteFile.find("/", i+1)
        # e.g. https://bla.com**/**xx
        firstNonProtoSlash = remoteFile.find("/", i+1)
        if firstNonProtoSlash != -1:
            f = remoteFile[firstNonProtoSlash + 1:]
            f = f.replace("/", "_")
            destFile = folderToStore + os.sep + f
        else:
            logging.error('   URL for remote file contains no valid usable file extension: {}'.format(remoteFile))
            return (False, remoteFile)
        r = requests.get(remoteFile, stream=True)
        if r.status_code != 200:
            logging.error("Error while downloading remote source: status={}".format(r.status_code))
            return (False, remoteFile)
        r.raw.decode_content = True
        with open(destFile, 'wb') as f:
            shutil.copyfileobj(r.raw, f)
        return (True, destFile)
    except Exception as e:
        logging.error("Error while downloading remote source: {}".format(e))
        return (False, remoteFile)


def _tryToFindTemplate(templateFile, args):
    """tests if the given file name is a external or an internal template. If it
    is an internal template, then the file name is changed to a relative path.

    Function return a tupel with the true or false as first element, and the file path
    to the found file as second element
    """

    fileExists = False
    templateFileToReturn = templateFile
    if doesFileExist(templateFile):
        fileExists = True
    elif templateFile.startswith("http://") or templateFile.startswith("https://"):
        # load template from the remote location and store it in a temp folder
        folderToStore = args.folder2StoreTemplates if args.folder2StoreTemplates else tempfile.gettempdir()
        (fileExists, templateFileToReturn) = _getFileFromRemoteSource(templateFile, folderToStore, args.delExistingStoredTemplates)
    else:
        internalTemplateName = 'yacg/generators/templates/{}.mako'.format(templateFile)
        fileExists = doesFileExist(internalTemplateName)
        templateFileToReturn = internalTemplateName
    fileExistsString = getOkTxt('found') if fileExists else getErrorTxt('missing')
    logging.info('   {}\t{}'.format(fileExistsString, templateFile))
    return (fileExists, templateFileToReturn)


def _foundAllModels(codeGenerationJobs, args):
    """checks up if all model file are accessible. For internal templates the
    template file name is changed

    returns True if all templates are available, else False
    """

    foundAll = True
    for job in codeGenerationJobs:
        for model in job.models:
            if model.schema.startswith("http://") or model.schema.startswith("https://"):
                folderToStore = args.folder2StoreModels if args.folder2StoreModels else tempfile.gettempdir()
                (fileExists, localModelFile) = _getFileFromRemoteSource(model.schema, folderToStore, args.delExistingStoredModels)
                if fileExists:
                    model.schema = localModelFile
            else:
                fileExists = doesFileExist(model.schema)
            fileExistsString = getOkTxt('found') if fileExists \
                else getErrorTxt('missing')
            if not fileExists:
                foundAll = False
            logging.info('   {}\t{}'.format(fileExistsString, model.schema))
    return foundAll


def _isConfigurationValid(codeGenerationJobs, args):
    """checks up the give job configuration array and
    returns True if valid else if not
    """

    isValid = True
    if (codeGenerationJobs is None) or (len(codeGenerationJobs) == 0):
        errorMsg = getErrorTxt('no generation jobs are given - cancel')
        logging.info(errorMsg)
        return False
    if _foundAllTemplates(codeGenerationJobs, args) is False:
        isValid = False
    if _foundAllModels(codeGenerationJobs, args) is False:
        isValid = False
    return isValid


def __handleNotUniqueTypeNames(loadedTypes, failIfTypeNamesNotUnique, makeMultipleTypeNamesUnique, noLogs):
    notUniqueNames = modelFuncs.getNotUniqueTypeNames(loadedTypes)
    if makeMultipleTypeNamesUnique:
        modelFuncs.makeTypeNamesUnique(loadedTypes, notUniqueNames)
        logging.info("there were some not unique type names loaded, made them unique: {}".format(notUniqueNames))
        return False
    if (len(notUniqueNames) > 0) and (not noLogs):
        logMsg = " THERE ARE NOT UNIQUE TYPE NAMES: {}".format(notUniqueNames)
        if failIfTypeNamesNotUnique:
            logging.error(logMsg)
        else:
            logging.info(logMsg)
    return (len(notUniqueNames) > 0) and failIfTypeNamesNotUnique


def __handleOnlyWithTopLevelTypes(allLoadedTypes, args):
    if args.goOnlyWithTopLevelTypes:
        tmpTypes = []
        for t in allLoadedTypes:
            if hasattr(t, "topLevelType") and t.topLevelType:
                tmpTypes.append(t)
        return tmpTypes
    return allLoadedTypes


def __handleRemoveArrayTypesFromTopLevel(allLoadedTypes, args):
    if args.removeArrayTypesFromTopLevel:
        tmpTypes = []
        for t in allLoadedTypes:
            if not isinstance(t, ArrayType):
                tmpTypes.append(t)
        return tmpTypes
    return allLoadedTypes


def __handleRemoveDictionaryTypesFromTopLevel(allLoadedTypes, args):
    if args.removeDicitonaryTypesFromTopLevel:
        tmpTypes = []
        for t in allLoadedTypes:
            if not isinstance(t, DictionaryType):
                tmpTypes.append(t)
        return tmpTypes
    return allLoadedTypes



def __doCodeGen(codeGenerationJobs, args):
    """process the jobs to do the actual code generation
    """
    previousCodeGenMetaData = protocolFuncs.getPreviousMetaData(args.protocolFile, args.noLogs)
    previousJobsMetaData = previousCodeGenMetaData.get("jobs", {})
    codeGenMetaData = {}
    jobsMetaData = {}
    codeGenMetaData["date"] = datetime.now().strftime("%d-%m-%Y %H:%M:%S.%f")
    codeGenMetaData["jobs"] = jobsMetaData
    allSkipped = True
    jobIndex = 1
    for job in codeGenerationJobs:
        allLoadedTypes = readModels(job, args.flattenInheritance)
        modelMetaData = protocolFuncs.getModelMetaData(allLoadedTypes, job.models[0].schema)
        jobName = job.name if job.name else "UNKNOWN_JOB_{}".format(jobIndex)
        jobsMetaData[jobName] = modelMetaData
        jobIndex = jobIndex + 1
        if __handleNotUniqueTypeNames(allLoadedTypes, args.failIfTypeNamesNotUnique, args.makeMultipleTypeNamesUnique, args.noLogs):  # noqa: E501
            sys.exit(1)

        if protocolFuncs.shouldSkipCodeGen(
                args.skipCodeGenIfVersionUnchanged,
                args.skipCodeGenIfMd5Unchanged,
                previousJobsMetaData,
                modelMetaData,
                jobName,
                args.noLogs) is True:
            if not args.noLogs:
                logging.info(" SKIP CODEGEN: {}".format(jobName))
            continue
        if not args.noLogs:
            logging.info(" do codeGen: {}".format(jobName))
        if args.skipCodeGenDryRun is True:
            if not args.noLogs:
                logging.info(" 'skipCodeGenDryRun' is set, so no codeGen is executed': {}".format(jobName))
            continue

        allSkipped = False
        loadedTypes = []
        loadedTypes = __handleOnlyWithTopLevelTypes(allLoadedTypes, args)
        loadedTypes = __handleRemoveArrayTypesFromTopLevel(loadedTypes, args)
        loadedTypes = __handleRemoveDictionaryTypesFromTopLevel(loadedTypes, args)

        for task in job.tasks:
            if task.singleFileTask is not None:
                renderSingleFileTemplate(
                    loadedTypes,
                    task.blackListed,
                    task.whiteListed,
                    task.singleFileTask)
            elif task.multiFileTask is not None:
                renderMultiFileTemplate(
                    loadedTypes,
                    task.blackListed,
                    task.whiteListed,
                    task.multiFileTask)
    if (not allSkipped) and (args.skipCodeGenDryRun is not True):
        protocolFuncs.writeProtocolFile(args.protocolFile, codeGenMetaData)


def __printUsedFiles(codeGenerationJobs, args):
    """process the jobs to do the actual code generation
    """

    usedFiles = []
    for job in codeGenerationJobs:
        loadedTypes = readModels(job, args.flattenInheritance)
        for type in loadedTypes:
            if isinstance(type, EnumType) or isinstance(type, ComplexType):
                if type.source is not None:
                    if type.source not in usedFiles:
                        usedFiles.append(type.source)
    if len(usedFiles) == 0:
        logging.info("No loaded files detected.")
        pass
    else:
        logging.info("The following files were loaded ...")
        for usedFile in usedFiles:
            logging.info("-> {}".format(usedFile))
            pass


def main():
    """starts the program execution"""
    args = parser.parse_args()
    codeGenerationJobs = getJobConfigurations(args)
    if not _isConfigurationValid(codeGenerationJobs, args):
        sys.exit(1)
    if args.usedFilesOnly:
        __printUsedFiles(codeGenerationJobs, args)
    else:
        __doCodeGen(codeGenerationJobs, args)


if __name__ == '__main__':
    main()
