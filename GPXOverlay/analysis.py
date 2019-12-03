import xml.etree.ElementTree as ET
import dateutil.parser
import numpy as np
from GPXOverlay import calculations

class Analysis:
    """Processes GPX file to get speed, elevation, and other data

    Attributes:
        gpx_data (str): Path to GPX file
        num_gps_points (int): Number of recorded GPS points (number of track
            points in track segment)
        time (ndarray): 1D array containing time measurements with type
            'datetime64[s]'
        elevation (ndarray): 1D array containing elevation measurements [m]
        velocity (ndarray): 1D array containing caculated velocity values [m/s]
    """

    def __init__(self, gpx_file):
        """ __init__ method for Analysis class

        Args:
            gpx_file (str): Path to GPX file
        """

        # import and parse GPX file
        self.gpx_data = gpx_file
        tree = ET.parse(self.gpx_data)
        root = tree.getroot()
        trkseg = root[1][2]

        self.num_gps_points = len(trkseg)
        self.time = np.full(self.num_gps_points, np.datetime64("NaT"), dtype='datetime64[s]')
        self.elevation = np.full(self.num_gps_points, np.nan)
        self.velocity = np.full(self.num_gps_points - 1, np.nan)

        # iterate through track points in track segment and perform calculations
        for i in range(len(trkseg)-1):
            trkpt1=trkseg[i]
            trkpt2=trkseg[i+1]

            lat1 = float(trkpt1.attrib["lat"])
            long1 = float(trkpt1.attrib["lon"])
            lat2 = float(trkpt2.attrib["lat"])
            long2 = float(trkpt2.attrib["lon"])

            # Gets elevation data from GPX file
            elevation = trkpt1[0].text

            # Gets time element from GPX file (ISO 8601 standard)
            time1 = dateutil.parser.parse(trkpt1[1].text)
            time2 = dateutil.parser.parse(trkpt2[1].text)

            # Only process and store uniue values into class variables.
            # Sometimes there will be identical values with the same time stamp
            if time1 != time2:
                v_m_s = calculations.calc_velocity(lat1, long1, time1, lat2, long2, time2) # m/s
                v_min_km = calculations.min_km(v_m_s) # min/km
                v_km_h = calculations.km_h(v_m_s) #km/h

                self.time[i] = time1
                self.elevation[i] = elevation
                self.velocity[i] = v_m_s

        # Filter all valid values (not NaN or NaT)
        self.time = self.time[np.logical_not(np.isnat(self.time))]
        self.elevation = self.elevation[np.logical_not(np.isnan(self.elevation))]
        self.velocity = self.velocity[np.logical_not(np.isnan(self.velocity))]

    @property
    def velocity_data(self):
        """Gets all calculated velocity values"""
        return self.velocity

    @ property
    def time_data(self):
        """Gets all time measurments"""
        return self.time

    @property
    def elevation_data(self):
        """Gets all elevation measurements"""
        return self.elevation
