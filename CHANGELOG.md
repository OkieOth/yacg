# 6.2.0
* enable http/s sources for templates
* enable http/s sources for models

# 6.1.0
* add additional functions to modelFuncs
* fix random date generation in a way, that it produces ISO strings

# 6.0.6
* improve the python bean template

# 6.0.5
* fix complex value type issue for dictionaries (issue139)

# 6.0.4
* prevent empty output from random gerenrated data

# 6.0.3
* add missing file to docker image
* fix error with wrong array sizes for random data, when defaultConfig.defaultElemCount is set

# 6.0.2
* fix error in random array handling
* fix errorn in handling of random dates
* increment defaultTypeDepth for random data generation

# 6.0.1
* improved GO template
* introduce `allTypes` switch to `createRandomData.py`
* add missing `createRandomData` and `randomDataServer` scripts to the docker image
* fix random data issues for uuids and enum types

# 6.0.0
* fix bug in golang template
* remove RandomDataGenerator from config and implementation
* add `createRandomData.py` script to create random data
* add `randomDataServer.py` script to deliver random data over http

# 5.9.5
* add command line switches for better handling of Dictionary- and ArrayTypes
* improve plantuml template
* improve top level type detection - even in an unperformant way xD

# 5.9.4
* fix bug for dictionaries in models that contains arrays as value

# 5.9.2 - 5.9.3
* CI fixes

# 5.9.1
* fix bug with not detected enum values, caused by a specific order of type declaration

# 5.9.0
* add file validation against a schema function to the package

# 5.8.2 - 5.8.4
* CI fixes

# 5.8.1
* fix bug with array constraints for nested arrays

# 5.8.0
* enable additional enum types: numeric, date, date-time, uuid, time

# 5.7.2
* fix nomalizeSchema bug for missing

# 5.7.1
* harden 'initFromDict' for non dictionary types

# 5.7.0
* add types with top-level '$ref' entry
* allow allOf for inner types

# 5.6.3
* removed AsyncApi PublishOperation type
* fix bugs in normalizeSchema

# 5.6.2
* introduce addtional switches for normalizeSchema
* fix bug in normalizeSchema

# 5.6.1
* bug fixes for parsing openapi files
* missing operationId doesn't hurt any longer
* add 'getTypeAndAllRelatedTypes' modelfunc

# 5.6.0
* tool to create normalized schemas

# 5.5.1
* fix error, that only the first tag with values is used

# 5.5.0
* add golang type template
* add modelFuncs func 'isComplexType'
* introduce ArrayType
* usage of top-level Array- and DictionaryTypes in the JSON schemas enabled


# 5.4.0
* Introduce Duration type

# 5.3.3
* modelFuncs: added function, which checks for property of type TimeType
* modelFuncs: added function where the target type can be provided as parameter.
* xsdFuncs: added handling for formats of IntegerType and NumberType
* xsdFuncs: added handling for ObjectType and BytesType

# 5.3.2
* javaFuncs: map array of ObjectType to *java.util.List\<Object\>*

# 5.3.1
* Added prefix to templateHelper.addLineBreakToDescription
  (and removed leading space from first line)

# 5.3.0
* Added TimeType to model

# 5.2.2
* Bugfix: update docker image to python:3.10-slim-buster

# 5.2.1
* Bugfix: read tags for enum types

# 5.2.0
* add additional commandline switch for domain black- and whitelists
* apply commandline black- and whitelists to the given configuration via file

# 5.1.0
* addes some convenience functions for Java templates

# 5.0.0
* add basic asyncapi support

# 4.7.0
* introduce config option and commandline switch for failing when there are not unique type names

# 4.6.0
* javaFuncs: added method to sanitize property named (class->clazz etc.) and another one to restore them at the end of the template

# 4.5.0
* javaFuncs: fixed typos
* javaFuncs: map to wrapper types Float and Long when applicable
* stringUtils: methods for converting *snake_case* to *CamelCase*
* modelFuncs: added some methods to work with the properties of a type (none recursive)

# 4.4.0
* Create missing directories for output files on singleFileGenerator 

# 4.3.1
* add model `hasPropertyWithTag`

# 4.3.0
* yacg commandline switch to protocol the codegen
* yacg commandline switch to skip codegen when model version hasn't change to the last protocolled run

# 4.2.0
* add typescript helper funcs
* enable plantuml template to visualize type and property tags
* introduce handling of multidimensional arrays

# 4.1.2
* fixed bug for x-enumValues

# 4.1.1
* add key related model funcs
* fix bug with 'additionalProperties'. From JSON schema specs this value can be boolean or object. The boolean version can't used before.

# 4.1.0
* add enum values

# 4.0.1
* add `doesTypeOrAttribContainsType` to modelFuncs

# 4.0.0
* extend x-ref/foreign key reference with a properties reference. **Attention** this may break some templates (e.g. plantUml)
* shows foreign key references in puml diagrams

# 3.4.1
* enable automatic releases with github actions

# 3.4.0
* enable http references in schemas

# 3.3.1
* fix 'allOf' bug in cases that a model is referenced multiple times

# 3.3.0
* add 'tasks' switch to yacg command line to include only named tasks in the codegen run
* add 'jobs' switch to yacg command line to include only named jobs in the codegen run
* add minLength, maxLength, pattern validation to StringType

# 3.2.5
* fix bug in calculating absolute filenames for referenced yaml files

# 3.2.4
* improve openApi templates
* model2yaml - remove alphabetical sorting of the output

# 3.2.3
* include also a latest container image into the CI

# 3.2.2
* move to GitHub container registry for publishing via CI

# 3.2.1
* improve Map handling in javaBeans template

# 3.2.0
* implement model support for dictionaries
* introduce pure object type

# 3.1.0
* improved Python object initialization - inspired by a contribution of Paul Way [https://github.com/PaulWay]

# 3.0.1
* fix bug when extracting formats for numbers and integers

# 3.0.0
* replace '__' prefix for custom extensions with 'x-' prefix
* add some modelFuncs to facilitate the usage of openApi models in templates

# 2.1.2
* fix a bug in handling single type models w/o any title

# 2.1.1
* put the new helper scripts to the docker image
* fix reference extentions to yaml or json depending the convertion

# 2.1.0
* modelToYaml script
* modelToJson script
* enable usage of stdin for modelTo[Json|Yaml] scripts

# 2.0.0
* rename ByteType to BytesType

# 1.4.0
* introduction of a ByteType

# 1.3.1
* add new funcs to stringUtils
* fix enum bug in python template

# 1.3.0
* add '--flattenInheritance' command line switch
* introduce 'yacgFlattenType' type tag
* introduce 'yacgIgnoreForModel' type tag

# 1.2.0
* add '--usedFilesOnly' command line switch

# 1.1.0
* add model version to complex types and enums
* add increment version script for json schemas
* mix in models given per cmd param into the file configuration

# 1.0.1
* bump dependency version

# 1.0.0
* add min/max handling for properties
* add original format string to the Properties type
* handle ordinal value in protobuf template

# 0.16.0
* enable generation of test data
* rename property attrib 'implicitRef' to 'foreignKey'
* introduce '__key' model extension, to mark properties as logical keys
* introduce '__visualKey' model extension, to mark properties as visual key (e.g. name, label, ...) 

# 0.15.0
* add protobuffer template
* add ordinal attribute to complex type properties

# 0.14.0
* implement required constraint for model attributes

# 0.13.0
* add krakend example

# 0.11.0
* fix error in the javaFuncs helper
* extend internal model with minItems and maxItems restrictions for array properties
* extend internal model with uniqueItems for array properties

# 0.10.0
* improvements for the Java bean template

# 0.9.0
* include implicit references for properties

# 0.8.1
* fix error in initializing additional vars from command line
* fix error for usages of global command line give template parameters

# 0.8.0
Yacg docker images can run as normal user.

# 0.7.0
Enable config file customization via env variables or command
line switches.
