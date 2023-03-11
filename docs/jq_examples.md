# Some examples for jq queries
```bash
# add test attrib to the object
cat resources/models/json/yacg_config_schema.json | jq '.definitions.BlackWhiteListEntry + {test: "hallo"}'

# add test attrib to a sub property
cat resources/models/json/yacg_config_schema.json | jq '.definitions.BlackWhiteListEntry | .properties += {test: "hallo"}'
```