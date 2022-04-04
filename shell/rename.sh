#!/bin/bash
for file in ./*
do
date: add_date.s
    if test -f "${file}"
    then
        inString=${file:2:10}
        sed -i "3a\date: $inString" "${file}"
    fi
done