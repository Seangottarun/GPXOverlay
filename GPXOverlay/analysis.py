import xml.etree.ElementTree as ET
import dateutil.parser
import numpy as np
from GPXOverlay import calculations

class Analysis:
    def __init__(self, gpx_file):
        self.gpx_data = gpx_file
        tree = ET.parse(self.gpx_data) # import xml file
        root = tree.getroot()

        trkseg = root[1][2]
        self.num_gps_points = len(trkseg)

        self.time = np.zeros(self.num_gps_points, dtype='datetime64[s]')
        self.velocity = np.zeros(self.num_gps_points - 1)

        for i in range(len(trkseg)-1):
            trkpt1=trkseg[i]
            trkpt2=trkseg[i+1]

            lat1 = float(trkpt1.attrib["lat"])
            long1 = float(trkpt1.attrib["lon"])
            lat2 = float(trkpt2.attrib["lat"])
            long2 = float(trkpt2.attrib["lon"])

            # Gets time element from GPX file (ISO 8601 standard)
            time1 = dateutil.parser.parse(trkpt1[1].text)
            time2 = dateutil.parser.parse(trkpt2[1].text)

            v_m_s = calculations.calc_velocity(lat1, long1, time1, lat2, long2, time2) # m/s
            v_min_km = calculations.min_km(v_m_s) # min/km
            v_km_h = calculations.km_h(v_m_s) #km/h

            self.time[i] = time1
            self.velocity[i] = v_m_s


    def get_velocity_data(self):
        return self.velocity
        #print(self.velocity)
        #print(len(self.velocity))

    def get_time_data(self):
        return self.time

    def get_positions(self):
        print(self.position)
