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
