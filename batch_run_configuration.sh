#!/bin/bash

# Rerun a configuration over x years, by simply Overwriting
# the value YEAR with the current year

template=$1


for year in $(seq 1988 2015); do
  echo $year
  sed -e "s/YEAR/$year/g" $template > tmp_config.json
  python3 run_configuration.py tmp_config.json -a
done
