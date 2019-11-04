"""This module calculates velocity given the latitude, longitude, and time from
two different points.

It assumes a perfectly spherical earth and defines the centre of the Earth to be
the origin of a 3D coordinate space. The location data of each point can then be
used to construct a 3D vector. Using the dot product and the arc length formula,
the surface distance between the 2 points can be calculated.
"""
import math
import xml.etree.ElementTree as ET

RADIUS_OF_EARTH = 6378 * 10**3 # radius of the earth [m]
SECONDS_IN_A_MINUTE = 60
SECONDS_IN_AN_HOUR = 3600
METRES_IN_A_KILOMETRE = 1000

def calc_position(latitude, longitude):
    """Returns position vector as a list of x-, y-, z- components given latitude
    and longitude

    Args:
        latitude (float): latitude of the position in degrees North/South of equator
        longitude (float): longitude of the position in degrees East/West of
            Prime Meridian

    Returns:
        A list of float values representing xyz coordinates of position vector1
        on 3D coordinate system with the centre of the earth as the origin.

    """
    lat = math.radians(latitude)
    long = math.radians(longitude)

    x_coord = RADIUS_OF_EARTH*math.cos(lat) * math.cos(long)
    y_coord = RADIUS_OF_EARTH*math.cos(lat) * math.sin(long)
    z_coord = RADIUS_OF_EARTH*math.sin(lat)

    return [x_coord, y_coord, z_coord]

def calc_angle(vector1, vector2):
    """Calculates angle between two position vectors

    Args:
        vector1 (list): list of x-,y-,z- components for 1st position
        vector2 (list): list of x-,y-,z- components for 2nd position

    Returns:
        The angle (float) in radians between the two 3D vectors

    """
    dot_prod = vector1[0] * vector2[0] + vector1[1] * vector2[1] + vector1[2] * vector2[2]
    cos_theta = dot_prod / RADIUS_OF_EARTH**2

    # Temp fix for domain errors with acos because of floating point errors.
    # Specifically an issue when vectors almost parallel or antiparallel, which
    # because of rounding, can give cos_theta > 1 or cos_theta < -1
    if cos_theta > 1:
        cos_theta = 1
    elif cos_theta < -1:
        cos_theta = -1

    return math.acos(cos_theta)

def calc_distance(latitude1, longitude1, latitude2, longitude2):
    """Calculates distance between 2 positions given latitude and longitude

    The angle between the 2 position vectors is first calculated and then the
    arc length equaiton is used to calculate distance (assume spherical Earth).

    Args:
        latitude1 (float): latitude of 1st position in degrees North/South of equator
        longitude1 (float): longitude of 1st position in degrees East/West of
            Prime Meridian
        latitude2 (float): latitude of 2nd position in degrees North/South of equator
        longitude2 (float): longitude of 2nd position in degrees East/West of
            Prime Meridian

    Returns:
        The distance (float) in metres between the 2 positions.

    """
    # use latitude and longitude to get two 3D vectors
    pos1 = calc_position(latitude1, longitude1)
    pos2 = calc_position(latitude2, longitude2)

    # calculate angle betw 2 position vectors using dot product
    theta = calc_angle(pos1, pos2)

    # calculate distance along Earth's surface using arc length eqn
    dist = RADIUS_OF_EARTH * theta
    return dist

def calc_velocity(latitude1, longitude1, time1, latitude2, longitude2, time2):
    """Calculates velocity between 2 points (position and time)

    Assumes that velocity is constant between the 2 recorded GPS points. As the
        difference in time between the 2 points approaches 0, the calculated
        velocity approaches the instantaneous velocity.

    Args:
        latitude1 (float): latitude of 1st position in degrees North/South of equator
        longitude1 (float): longitude of 1st position in degrees East/West of
            Prime Meridian
        time1 (float): elapsed time in seconds since the start of the GPS track
            to the 1st position
        latitude2 (float): latitude of 2nd position in degrees North/South of equator
        longitude2 (float): longitude of 2nd position in degrees East/West of
            Prime Meridian
        time2 (float): elapsed time in seconds since the start of the GPS track
            to the 2nd position

    Returns:
        The velocity (float) in metres/second in between the 2 positions.

    """
    delta_pos = calc_distance(latitude1, longitude1, latitude2, longitude2)
    delta_t = time2 - time1

    return delta_pos/delta_t.total_seconds()

def min_km(speed):
    """Converts speed in m/s to min/km"""
    if (speed==0): # return 0 to avoid division by 0
        return 0
    return (speed**-1) * (METRES_IN_A_KILOMETRE/SECONDS_IN_A_MINUTE)

def km_h(speed):
    """Converts speed in m/s to km/h"""
    return speed * (SECONDS_IN_AN_HOUR/METRES_IN_A_KILOMETRE)
