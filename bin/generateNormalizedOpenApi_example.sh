#!/bin/bash

scriptPos=${0%/*}

# script takes the yacg models and generate the program code
# based on them

pushd $scriptPos/.. > /dev/null

if ! python yacg.py \
    --noLogs \
    --models tests/resources/models/json/examples/openapi_v3_example_refs.json \
    --singleFileTemplates resources/templates/examples/normalizedOpenApiJson.mako=stdout \
    | python modelToYaml.py --stdin --dryRun
    then
    echo "    ERROR while create the stuff :-/"
    exit 1
fi

popd > /dev/null
