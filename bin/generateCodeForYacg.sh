#!/bin/bash

scriptPos=${0%/*}

# script takes the yacg models and generate the program code
# based on them

pushd $scriptPos/.. > /dev/null

echo "create meta model classes ..."
if ! pipenv run python3 yacg.py --model \
    resources/models/json/yacg_model_schema.json \
    --output stdout \
    --template pythonBeans; then
    echo "    ERROR while create meta model classes"
else
    echo "    done"
fi

popd > /dev/null