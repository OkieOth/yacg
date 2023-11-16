#!/bin/bash

scriptPos=${0%/*}

# script takes the yacg models and generate the program code
# based on them

pushd $scriptPos/.. > /dev/null

echo "create yacg demo code based on a config file ..."
if ! python yacg.py --config resources/configurations/gen_yacg_code.json; then
    echo "    ERROR while create the stuff :-/"
    exit 1
fi

popd > /dev/null
