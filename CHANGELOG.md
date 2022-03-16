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
