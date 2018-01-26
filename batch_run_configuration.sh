#!/bin/bash

# Rerun a configuration over x years, by simply Overwriting
# the value YEAR with the current year

template=$1

cnt=0

for year in $(seq 1988 2015); do
  echo $year
  ext=""
  if [[ $cnt -gt 1 ]]; then
    ext=" -a"
  fi
  sed -e "s/YEAR/$year/g" $template > tmp_config.json
  python3 run_configuration.py tmp_config.json $ext
  
  ((cnt+=1))
done
