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


def generate_overlay_frame(id, speed, time):
    """Generates all overlay frames using velocity and time data"""
    frame.generate_png(speed, time, id)

def convert_overlay_to_video(frame_name_format, output_overlay_path, fps=30):
    """Combines speed frames into a single video"""
    (
        ffmpeg
        .input(frame_name_format, framerate=fps)
        .output(output_overlay_path, vcodec='png')
        .run()
    )

def overlay_video(input_video, overlay_video, output_video_path, overlay_x_pos, overlay_y_pos):
    """Overlays video of speed progression onto input video and
    generates output video"""
    input_video = ffmpeg.input(input_video)
    overlay = ffmpeg.input(overlay_video)
    (
        ffmpeg
        .overlay(input_video, overlay, eof_action='repeat', x=overlay_x_pos, y=overlay_y_pos)
        .output(output_video_path)
        .run()
    )
