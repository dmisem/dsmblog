#!/usr/bin/env bash

DIR=`pwd`"/dsmblog/"
cd ${DIR}
CDT=`date +%Y-%m-%d\ %H:%M`  # Current datetime

git rm -rf .
git commit -m "Autoclear: ${CDT}"
git push
