#!/bin/bash

scriptPos=${0%/*}

# script takes the yacg models and generate the program code
# based on them

pushd $scriptPos/.. > /dev/null

echo "create meta model classes ..."
if ! pipenv run python3 yacg.py --models \
    resources/models/json/yacg_model_schema.json \
    --output ${scriptPos}/../yacg/model/genModel.py \
             ${scriptPos}/../tests/model/test_genModel.py \
    --templates pythonBeans \
                pythonBeansTests; then
    echo "    ERROR while create meta model classes"
    exit 1
fi

popd > /dev/null