#!/usr/bin/bash
ls single_results/* | sed -e "s/_/\t/g" > results.tsv
