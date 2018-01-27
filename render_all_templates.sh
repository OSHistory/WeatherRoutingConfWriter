#!/bin/bash 

rm ~/.opencpn/plugins/weather_routing/ConfigFilePaths.xml

for template in conf/*txt; do 
    bash batch_run_configuration.sh $template 
done 
