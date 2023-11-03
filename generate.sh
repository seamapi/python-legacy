#!/usr/bin/env bash



mkdir -p ./generated
npx nextlove-sdk-generator generate python ./generated

rm -rf ./seamapi
cp -r ./generated/seamapi ./seamapi
