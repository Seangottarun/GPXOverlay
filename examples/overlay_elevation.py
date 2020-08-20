from GPXOverlay import analysis
from GPXOverlay import overlay
import matplotlib.pyplot as plt
import numpy as np
import imgkit

def main():
    # load GPX file into an Overlay object and provide a path for output video
    elevation_overlay = overlay.Overlay('sample-data-short.gpx', 'video.mp4')
    elevation_overlay.generate_elevation_frames()
    elevation_overlay.convert_elevation_frames_to_video()
    elevation_overlay.overlay_elevation()

main()
