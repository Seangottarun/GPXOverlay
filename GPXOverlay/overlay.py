""" This module defines the Overlay class used to generate the overlay frames and
the output video.
"""
import ffmpeg
import xml.etree.ElementTree as ET
import dateutil.parser
import imgkit
import numpy as np
import os

from GPXOverlay import frame
from GPXOverlay import calculations
from GPXOverlay import analysis

class Overlay():
    """Generates output video with overlayed data

    Attributes:
        gpx_data (str): Path to GPX file
        video (str): Path to input video file
    """

    def __init__(self, gpx_data, input_video):
        """ __init__ method for Analysis class

        Args:
            gpx_file (str): Path to GPX file
            video (str): Path to input video file
        """
        self.video = input_video
        self.gpx_data = gpx_data

        if not os.path.exists('temp'):
            os.makedirs('temp')

    def generate_overlay_frames(self):
        """Generates all overlay frames using velocity and time data"""
        data = analysis.Analysis(self.gpx_data)
        times = data.time_data
        velocities = data.velocity_data

        for i, (velocity, time) in enumerate(zip(velocities, times)):
            frame.generate_png(velocity, time, i)

    def generate_elevation_frames(self):
        """Generates all overlay frames using elevation and time data"""
        data = analysis.Analysis(self.gpx_data)
        ele = data.elevation_data

        x = np.linspace(0,ele.size-1,ele.size)
        avg = np.average(ele) * np.ones(ele.size)
        y_min = np.amin(ele)
        y_max = np.amax(ele)
        y_min_array = y_max * np.ones(ele.size)
        y_max_array = y_min * np.ones(ele.size)

        for i in range(ele.size):
            frame.graph_elevation(x[0:i],ele[0:i], ele.size, avg, y_min, y_max)
            frame.generate_elevation_frame(i)


    def convert_elevation_frames_to_video(self):
        """Combines elevation frames into a single video"""
        (
            ffmpeg
            .input('temp/elevation%d.png', framerate=30)
            .output('temp/elevation_overlay.mp4', vcodec='png')
            .run()
        )

    def overlay_elevation(self):
        """Overlays video of elevation progression onto input video and
        generates output video"""
        input_video = ffmpeg.input(self.video)
        overlay = ffmpeg.input('temp/elevation_overlay.mp4')
        (
            ffmpeg
            .overlay(input_video, overlay, eof_action='repeat', x=25, y=25)
            .output('test_elevation.mp4')
            .run()
        )


    def convert_overlay_to_video(self):
        """Combines speed frames into a single video"""
        (
            ffmpeg
            .input('temp/speed%d.png', framerate=30)
            .output('temp/speed_overlay.mp4', vcodec='png')
            .run()
        )

    def overlay_video(self):
        """Overlays video of speed progression onto input video and
        generates output video"""
        input_video = ffmpeg.input(self.video)
        overlay = ffmpeg.input('temp/speed_overlay.mp4')
        (
            ffmpeg
            .overlay(input_video, overlay, eof_action='repeat', x=25, y=25)
            .output('test_speed.mp4')
            .run()
        )
