# General
This document describes the standard extension that are implemented in the
model parser. They should provide more clarity and flexibility ... in every
case in full respect of the existing standard.

# JSON-Schema Extensions
## Type and Property Tags
It's possible to tag types and properties for the later handling in the templates. To do this 
include a '__tag' attribute in your model. This attribute expects an array of strings as value.

```json
            "properties": {
                "name": {
                    "description": "type unique identifier",
                    "type": "string",
                    "__tags": ["constructorValue"]
                },
                ...
```

## Implicit type references
To put a reference to an foreign key like attribute, the '__ref' entry can be used. The
expected value it the same as for the '$ref' entry.

```json
        ...
        "TwoType": {
            "type": "object",
            "properties": {
                "aDate": {
                    "type": "string",
                    "format": "date-time"
                },                
                "aBool": {
                    "type": "boolean"
                },
                "aRef": {
                    "$ref": "./single_type_schema.json#/definitions/AnotherType"
                },
                "implicitRef": {
                    "type": "string",
                    "format": "uuid",
                    "__ref": "./single_type_schema.json#/definitions/AnotherType"
                }
            }
            ...
```

It is internally mapped to `yacg_model_schema->Property->implicitReference`.

## Domain information for the model
To specify a domain for a model use the '__domain' entry.

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "yacg file configuration",
  "description": "description of the file configuration for yacg",
  "version": "0.0.1",
  "__domain": "yacg.model.config",
  "definitions": {
 ```

## Property Ordinal Number
A custom keyword '__ordinal' can be used to add some kind of an index to 
a property definition. This index can be used for instance as field number when utilize yacg to generate protobuffer.

```json
        ...
        "TwoType": {
            "type": "object",
            "properties": {
                "aDate": {
                    "type": "string",
                    "format": "date-time",
                    "__ordinal": 1
                },                
                "aBool": {
                    "type": "boolean",
                    "__ordinal": 2
                },
                "aRef": {
                    "$ref": "./single_type_schema.json#/definitions/AnotherType",
                    "__ordinal": 3
                },
                "implicitRef": {
                    "type": "string",
                    "format": "uuid",
                    "__ref": "./single_type_schema.json#/definitions/AnotherType",
                    "__ordinal": 4
                }
            }
            ...
```


# OpenApi Extensions
## Authorization
On command level is it possible to specify roles that are allowed to access
this path and execute the given command on it. This extension doesn't a help
with resources authorization.

```yaml
  /tag:
    get:
      tags:
        - Tag
      description: Returns a list of Tag entries
      operationId: getTag
      # extention ...
      x-security:
        # scopes defined to get access
        scopes: 
          - 'test'
          - 'schnulli'
      responses:
        '200':
          description: successful operation
          content:
            application/xml:
              schema:
                $ref: '#/components/schemas/Tag'
            application/json:
              schema:
                $ref: '#/components/schemas/Tag'
```

The content of x-security->scopes is mapped on `yacg_openapi_paths->Command->security->scopes`