#!/bin/bash

scriptPos=${0%/*}

# script takes the yacg models and generate the program code
# based on them

pushd $scriptPos/.. > /dev/null

echo "create yacg demo code based on a config file ..."
if ! pipenv run python3 yacg.py --models resources/models/json/yacg_model_schema.json \
         --config resources/configurations/random_data_example_without_model.json; then
    echo "    ERROR while create the stuff :-/"
    exit 1
fi

popd > /dev/null