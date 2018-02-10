#!/bin/bash

# Rerun a configuration over x years, by simply Overwriting
# the value YEAR with the current year

template=$1


for year in $(seq 1988 2015); do
  echo $year
  for month in $(seq 1 1 12); do
    echo -e "\t$month"
    if [ $month -le 9 ]; then
      month_str="0"$month;
    else
      month_str=$month;
    fi

    sed \
      -e "s/YEAR/$year/g" \
      -e "s/MONTH_NUM/$month/g" \
      -e "s/MONTH_STR/$month_str/g" $template > tmp_config.json
    exit
    python3 run_configuration.py tmp_config.json -a
  done
done
