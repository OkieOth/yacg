#!/bin/bash

scriptPos=${0%/*}

# script takes the yacg models and generate some java stups (not working in the moment)
# This is basically an example for using multi-file generators from command line

pushd $scriptPos/.. > /dev/null

echo "create meta model cconfiglasses ..."
if ! pipenv run python3 yacg.py --models \
    resources/models/json/yacg_model_schema.json \
    --multiFileTemplates ${scriptPos}/../resources/templates/examples/javaBeans.mako=${scriptPos}/../tmp/cmdJavaBeans \
    --templateParameters modelPackage=de.test.model \
                         title="yacg model" \
                         destFileExt="java"; then
    echo "    ERROR while create Java classes"
    exit 1
fi

popd > /dev/null