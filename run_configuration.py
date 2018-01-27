
"""
Run a json-configuration file to produce opencpn-configuration output
"""

import argparse
import datetime
import json
import os

import lxml.etree as etree

from conf_writer import ConfWriter, Configuration

ap = argparse.ArgumentParser(
    description="""Run a configuration file and generate an opencpn
        configuration xml file""")

ap.add_argument("-a", "--append",
                dest="append",
                action="store_true",
                default=False)

ap.add_argument("configuration_file")
args = ap.parse_args()

conf_file = args.configuration_file

with open(conf_file) as fh:
    conf_data = json.load(fh)

CONFIG_FILE = os.path.join(
    os.path.expanduser("~"),
    ".opencpn/plugins/weather_routing/ConfigFilePaths.xml"
)

# Reload existing root or create new one
if args.append:
    if os.path.exists(CONFIG_FILE):
        config_doc = etree.parse(CONFIG_FILE)
        config_root = config_doc.getroot()
    else:
        config_root = etree.Element("BatchRoutingConfig")
else:
    config_root = etree.Element("BatchRoutingConfig")


base_dir = conf_data["path"]["base_dir"]
if not os.path.exists(base_dir):
    os.makedirs(base_dir)

start = conf_data["time"]["start_date"]
end = conf_data["time"]["end_date"]

start_date = datetime.datetime(start[0], start[1], start[2], start[3])
stop_date = datetime.datetime(end[0], end[1], end[2], end[3])
hour_increment = conf_data["time"]["hour_increment"]

routes = conf_data["routes"]
positions = conf_data["positions"]

for route in routes:
    print(route[0] + " => " + route[1])
    cw = ConfWriter()
    if route[0] not in positions:
        print("Could not find starting point!")
        continue
    if route[1] not in positions:
        print("Could not find end point!")
        continue

    cw.add_position(route[0], positions[route[0]][0], positions[route[0]][1])
    cw.add_position(route[1], positions[route[1]][0], positions[route[1]][1])

    curr_date = start_date

    while (curr_date < stop_date):
        conf = Configuration(route[0], route[1], curr_date)
        conf.dt = route[2] * 3600   # iso-chron-timestep

        for key in conf_data["ocpn"]:
            if key == "boat":
                conf_data["ocpn"]["boat"] = os.path.join(
                    os.path.expanduser("~"),
                    ".opencpn/plugins/weather_routing/",
                    conf_data["ocpn"]["boat"]
                )
            conf.__dict__[key] = str(conf_data["ocpn"][key])

        cw.add_configuration(conf)
        curr_date += datetime.timedelta(0, hour_increment * 60 * 60)

    file_name = os.path.join(
        base_dir,
        route[0] + "_" + route[1] + conf_data["suffix"] + ".xml"
    )

    curr_route_config = etree.SubElement(config_root, "RouteConfig")
    curr_route_config_path = etree.SubElement(curr_route_config, "ConfigPath")
    curr_route_config_path.text = file_name
    curr_route_config_grib = etree.SubElement(curr_route_config, "GribPath")
    curr_route_config_grib.text = conf_data["time"]["grib_file"]

    cw.export_to_file(file_name)


with open(CONFIG_FILE, "wb+") as fh:
    fh.write(b'<?xml version="1.0" encoding="utf-8" ?>\n')
    fh.write(
        etree.tostring(
            config_root,
            encoding="utf-8",
            pretty_print=True)
    )
