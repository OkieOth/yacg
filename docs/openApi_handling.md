# General
yacg can handle openApi and swagger files to parse models from it.

In addition to the normal model extraction from 'definitions' and 
'components/schema' sections also the path sections are parsed.

Paths will be parsed as internal `openapi.PathType` objects. Currently
existing some limitations in the parsing of the PathTypes. References
to pre-defined, even external types, can be used, but inline declarations
of types inside of paths are not handled in the moment. See the examples
below.

Not working example:
```json
...
          "requestBody": {
            "content": {
              "application/x-www-form-urlencoded": {
                "schema": {
                  "properties": {
                    "name": {
                      "type": "string",
                      "description": "Updated name of the pet"
                    },
                    "status": {
                      "type": "string",
                      "description": "Updated status of the pet"
                    }
                  }
                }
              }
            }
          },
...
```
Working replacement with separate declaration:
```json
...
          "requestBody": {
                "content": {
                    "application/x-www-form-urlencoded": {
                        "schema": {
                            "$ref": "#/components/schemas/MyBodyParam"
                        }
                    }
                }
            },
...
    "components": {
      "schemas": {
        "MyBodyParam": {
            "type": "object",
            "properties": {
            "name": {
                "type": "string",
                "description": "Updated name of the pet"
            },
            "status": {
                "type": "string",
                "description": "Updated status of the pet"
            }
        },
...
```