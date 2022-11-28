# General
Goal is the generate random data from a given JSON schema.

The general approach is to annotate a given model with configurations for random
data generation and let then in a second step the script createRandomData.py
process the configuration

## Configuration
JSON schemas can be extended with specific configurations [see here](../resources/models/json/yacg_random_data_types.json). The extension can be put on types and attributes after an
attribute `x-processing`

```json
{
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Info Section",
    "description": "Info section for API definition specs as openapi and ayncapi",
    "version": "0.1.0",
    "x-domain": "yacg.model.shared.info",
    "type": "object",
    "properties": {
        "title": {
            "type": "string"
        },
        "version": {
            "type": "string"
        },
        "description": {
            "type": "string",
            "x-processing": {
                "randValueConf": {
                    "stringTypeConf": {
                        "strType": "TEXT",
                        "maxLength": 200
                    }
                }
            }
        },
        "license": {
            "type": "string",
            "x-processing": {
                "randIgnore": true
            }
        }
    },
    "x-processing": {
        "$comment": "includes this element in the random data creation, one element will be generated",
        "randElemCount": 1
    }

}
```

# Examples to use the jq command to annotate JSON schemas
## Include specific types in the random data generation