#!/usr/bin/env bash

DIR=`pwd`"/dsmblog/.git"
# cd ${DIR}
CDT=`date +%Y-%m-%d\ %H:%M`  # Current datetime
GT="git --git-dir=${DIR} "

${GT}rm -rf . && ${GT}commit -m "Autoclear: ${CDT}" && ${GT}push

pelican -o dsmblog content
 
${GT}add . && ${GT}commit -m "Autogenerate: ${CDT}" && ${GT}push
