#!/usr/bin/env bash

mkdir -p ./generated

if [ "$1" == "--dev" ]; then
  # Use the nextlove-sdk-generator from the parent directory
  cd ../nextlove-sdk-generator && npm run generate:python-sdk
  rm -rf ./seamapi
  cp -r ../nextlove-sdk-generator/output/python/seamapi ../python
else
  # Use Global Nextlove SDK Generator
  npx nextlove-sdk-generator generate python ./generated
  rm -rf ./seamapi
  cp -r ./generated/seamapi ./seamapi
fi
