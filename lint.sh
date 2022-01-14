#!/bin/bash

out=lint.log
echo -n >$out

for file in *py
    pylint $file |
    grep -v bad-indentation |
    grep -v "conform to snake_case naming" |
    grep -v missing-function-docstring |
    grep -v redefined-outer-name |
    grep -vi "conform to UPPER_CASE naming" |
    grep -v missing-module-docstring |
    cat >>$out

cat $out
