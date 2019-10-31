import ffmpeg
import xml.etree.ElementTree as ET
import dateutil.parser
import cProfile

import frame
import calculations

import imgkit

def generate_overlay_frames():
    tree = ET.parse('sample-data.gpx') # import xml file
    root = tree.getroot()

    trkseg = root[1][2]

    for i in range(200):#len(trkseg)-1):
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

        frame.generate_png(v_km_h, time1, i)
    return True

def convert_overlay_to_video():
    (
        ffmpeg
        .input('temp/*.png', pattern_type='glob', framerate=30)
        .output('temp.mp4', vcodec='png')
        .run()
    )

def overlay_video():
    input_video = ffmpeg.input('video.mp4')
    overlay = ffmpeg.input('temp.mp4')
    (
        ffmpeg
        .overlay(input_video, overlay, eof_action='repeat', x=25, y=25)
        .output('test_movie.mp4')
        .run()
    )
