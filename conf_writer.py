
from datetime import datetime
import os

import lxml.etree as etree


class ConfWriter():

    def __init__(self):
        VERSION = "1.11"
        CREATOR = "Opencpn Weather Routing plugin"
        self._root = etree.Element("OpenCPNWeatherRoutingConfiguration")
        self._root.attrib["version"] = VERSION
        self._root.attrib["creator"] = CREATOR

    def add_position(self, name, lat, lon):
        route_node = etree.SubElement(self._root, "Position")
        route_node.attrib["Name"] = name
        route_node.attrib["Latitude"] = str(lat)
        route_node.attrib["Longitude"] = str(lon)

    def add_configuration(self, conf_object):
        conf_node = conf_object._render_to_node()
        self._root.append(conf_node)

    def export_to_file(self, file_path):
        with open(file_path, "w+") as fh:
            fh.write('<?xml version="1.0" encoding="utf-8" ?>\n')
            fh.write(etree.tostring(self._root, pretty_print=True, encoding="UTF-8").decode("UTF-8"))
            fh.flush()


class Configuration():


    #def __init__(self, start, end, start_date, start_time):
    def __init__(self, start, end, start_datetime):

        self.start = start
        self.start_date = self._get_date_string(start_datetime)
        self.start_time = self._get_time_string(start_datetime)
        self.end = end


        # Optional Settings (set default vals here)
        self.dt = "14400"
        self.boat = os.path.join(os.path.expanduser("~"), ".opencpn/plugins/weather_routing/Boat.xml")
        self.integrator = "0"
        self.max_diverted_course = "90"
        self.max_course_angle = "180"
        self.max_search_angle = "120"
        self.max_true_wind_knots = "100"
        self.max_apparent_wind_knots = "100"
        self.max_swell_meters = "20"
        self.max_latitude = "90"
        self.tacking_time = "0"
        self.wind_vs_current = "0"
        self.avoid_cyclone_tracks = "0"
        self.cyclone_months = "1"
        self.cyclone_days = "0"
        self.use_grib = "1"
        self.climatology_type = "0"
        self.allow_data_deficient = "0"
        self.allow_wind_strength = "1" # note: in xml called: WindStrength
        self.detect_land = "1"
        self.detect_boundary = "0"
        self.currents = "0"
        self.inverted_regions = "0"
        self.anchoring = "0"
        self.from_degree = "0"
        self.to_degree = "180"
        self.by_degrees = "5"

    def _get_date_string(self, dt):
        month = str(dt.month).rjust(2, "0")
        day = str(dt.day).rjust(2, "0")
        year = str(dt.year)
        return "-".join([year, month, day])

    def _get_time_string(self, dt):
        hour = str(dt.hour).rjust(2, "0")
        minute = str(dt.minute).rjust(2, "0")
        sec = str(dt.second).rjust(2, "0")
        return ":".join([hour, minute, sec])


    def _render_to_node(self):
        node = etree.Element("Configuration")
        node.attrib["Start"] = str(self.start)
        node.attrib["StartDate"] = str(self.start_date)
        node.attrib["StartTime"] = str(self.start_time)
        node.attrib["End"] = str(self.end)
        node.attrib["dt"] = str(self.dt)
        node.attrib["Boat"] = str(self.boat)
        node.attrib["Integrator"] = str(self.integrator)
        node.attrib["MaxDivertedCourse"] = str(self.max_diverted_course)
        node.attrib["MaxCourseAngle"] = str(self.max_course_angle)
        node.attrib["MaxSearchAngle"] = str(self.max_search_angle)
        node.attrib["MaxTrueWindKnots"] = str(self.max_true_wind_knots)
        node.attrib["MaxApparentWindKnots"] = str(self.max_apparent_wind_knots)
        node.attrib["MaxSwellMeters"] = str(self.max_swell_meters)
        node.attrib["MaxLatitude"] = str(self.max_latitude)
        node.attrib["TackingTime"] = str(self.tacking_time)
        node.attrib["WindVSCurrent"] = str(self.wind_vs_current)
        node.attrib["AvoidCycloneTracks"] = str(self.avoid_cyclone_tracks)
        node.attrib["CycloneMonths"] = str(self.cyclone_months)
        node.attrib["CycloneDays"] = str(self.cyclone_days)
        node.attrib["UseGrib"] = str(self.use_grib)
        node.attrib["ClimatologyType"] = str(self.climatology_type)
        node.attrib["AllowDataDeficient"] = str(self.allow_data_deficient)
        node.attrib["WindStrength"] = str(self.allow_wind_strength)
        node.attrib["DetectLand"] = str(self.detect_land)
        node.attrib["DetectBoundary"] = str(self.detect_boundary)
        node.attrib["Currents"] = str(self.currents)
        node.attrib["InvertedRegions"] = str(self.inverted_regions)
        node.attrib["Anchoring"] = str(self.anchoring)
        node.attrib["FromDegree"] = str(self.from_degree)
        node.attrib["ToDegree"] = str(self.to_degree)
        node.attrib["ByDegrees"] = str(self.by_degrees)
        return node
