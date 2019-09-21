import math

R_e = 6378*10^3 # equatorial radius of the earth [m]

alpha_1 = 30 # latitude of 1st position vector [degrees]
beta_1 = 60 # longitude of 1st position vector [degrees]
alpha_2 = 40 # latitude of 2nd position vector [degrees]
beta_2 = 50 # longitutde of 2nd position vector [degrees]

def radians(angle):
    return angle*(math.pi/180)

def x_coord(latitude, longitude):
    return R_e*math.cos(latitude)*math.cos(longitude)

def y_coord(latitude, longitude):
    return R_e*math.cos(latitude)*math.sin(longitude)

def z_coord(latitude, longitude):
    return R_e*math.sin(latitude)

def position(latitude, longitude): # returns list representing position vector
    return [x_coord(latitude, longitude), y_coord(latitude, longitude), z_coord(latitude, longitude)]

def dot(vector1, vector2): # performs dot product
    result = []
    if len(vector1)!=len(vector2): # check if vectors same length
        return False
    for i in len(vector1):  # multiply vectors elementwise and concat to result
        result += [vector1[i] * vector2[i]]
    return result

def angle(vector1, vector2):
    cos_theta = dot(vector1, vector2) / R_e^2
    return math.arccos(cos_theta)

def distance(angle):
    return R_e * angle;

def calc_distance(latitude1, longitude1, latitude2, longitude2):
    # calculates velocity from GPX file using latitude, longitude, and time data
    # assume a perfectly spherical earth
    # define origin of xyz coordinates as the centre of the earth

    # convert latitude and longitude into radians
    lat1 = radians(latitude1)
    long1 = radians(longitude1)

    lat2 = radians(latitude2)
    long2 = radians(longitude2)

    # use latitude and longitude to get two 3D vectors
    position1 = position(lat1, long1)
    position2 = position(lat2, long2)

    # calculate angle betw 2 position vectors using dot product
    theta = angle(position1, position2)

    # calculate displacement using arc length eqn
    displacement = distance(theta)

    # find velocity by displacement/time

    return distance

calc_distance()
