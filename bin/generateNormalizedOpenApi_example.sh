#!/bin/bash

scriptPos=${0%/*}

# script takes the yacg models and generate the program code
# based on them

pushd $scriptPos/.. > /dev/null

if ! pipenv run python3 yacg.py \
    --noLogs \
    --models tests/resources/models/json/examples/openapi_v3_example_refs.json \
    --singleFileTemplates resources/templates/examples/normalizedOpenApiJson.mako=stdout \
    | pipenv run python3 modelToYaml.py --stdin --dryRun
    then
    echo "    ERROR while create the stuff :-/"
    exit 1
fi

popd > /dev/null