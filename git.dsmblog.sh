#!/usr/bin/env bash

DIR=`pwd`"/dsmblog"
CDT=`date +%Y-%m-%d\ %H:%M`  # Current datetime
GT="git --git-dir=${DIR}/.git --work-tree=${DIR} "

pelican -o dsmblog content
echo Generated

if [[ $# -eq 0 ]]; then
    ${GT}add . && ${GT}commit -a -m "Autogenerate: ${CDT}" && ${GT}push
    echo Pushed!
fi
