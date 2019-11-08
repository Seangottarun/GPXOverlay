import ffmpeg
import xml.etree.ElementTree as ET
import dateutil.parser
import cProfile

from GPXOverlay import frame
from GPXOverlay import calculations
from GPXOverlay import analysis

import imgkit

class Overlay():
    def __init__(self, gpx_data, input_video, ):
        self.video = input_video
        self.gpx_data = gpx_data

    def generate_overlay_frames(self):
        data = analysis.Analysis(self.gpx_data)
        times = data.get_time_data()
        velocities = data.get_velocity_data()

        for i, (velocity, time) in enumerate(zip(velocities, times)):
            frame.generate_png(velocity, time, i)
        return True

    def convert_overlay_to_video(self):
        (
            ffmpeg
            .input('temp/*.png', pattern_type='glob', framerate=30)
            .output('temp.mp4', vcodec='png')
            .run()
        )

    def overlay_video(self):
        #input_video = ffmpeg.input('video.mp4')
        input_video = ffmpeg.input(self.video)
        overlay = ffmpeg.input('temp.mp4')
        (
            ffmpeg
            .overlay(input_video, overlay, eof_action='repeat', x=25, y=25)
            .output('test_movie.mp4')
            .run()
        )
