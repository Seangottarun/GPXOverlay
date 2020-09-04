import os
import multiprocessing
import time
import ffmpeg
import numpy as np
from scipy.interpolate import interp1d

from GPXOverlay import analysis
from GPXOverlay.overlay import *
from GPXOverlay import frame
from GPXOverlay.utils import round_fraction_to_nearest_int

"""
def main():
    # load GPX file into an Overlay object and provide a path for output video
    speed_overlay = overlay.Overlay('sample-data-short.gpx', 'video.mp4')
    speed_overlay.generate_overlay_frames()
    speed_overlay.convert_overlay_to_video()
    speed_overlay.overlay_video()
main()
"""

if __name__ == '__main__':
    start = time.time()
    gpx_file = 'sample-data.gpx'
    data = analysis.Analysis(gpx_file)
    time_points = data.time_data
    velocities = data.velocity_data
    input_video = 'video.mp4'

    # Get video data required for interpolation
    probe = ffmpeg.probe(input_video)
    video_info = next(s for s in probe['streams'] if s['codec_type'] == 'video')
    width = int(video_info['width'])
    height = int(video_info['height'])
    num_frames = int(video_info['nb_frames'])

    # Perform interpolation since GPS sample rate and video frame rate are
    # different. This generates intermediate GPS points to overlay on the video
    # frames (assuming the usual 1Hz GPS sample rate and 30 fps video frame rate)

    # Frame rate is given as a string containing a fraction
    # TODO: check if rounding up to 30 fps from 29.97 fps is an issue
    frame_rate = round_fraction_to_nearest_int(video_info['avg_frame_rate'])

    # Currently the time data is not interpolated and is just repeated for all
    # frames in the same second of video playback. This is just to avoid dealing
    # with date and time formats
    interpolated_time_points = np.repeat(time_points, frame_rate)
    interpolated_time_points = interpolated_time_points[:num_frames]

    # Create dummy points used for independent variables in interpolation
    original_points = np.linspace(0, len(time_points) - 1, len(time_points))
    interpolated_points = np.linspace(0, len(time_points) - 1, num_frames)

    f_interpolate = interp1d(original_points, velocities, kind='cubic')
    interpolated_velocities = f_interpolate(interpolated_points)

    if not os.path.exists('temp'):
        os.makedirs('temp')

    # Create a pool with same number of worker processes as number of cpu cores
    pool = multiprocessing.Pool()

    for i, (velocity, time_point) in enumerate(zip(interpolated_velocities, interpolated_time_points)):
        # Generate each overlay frame asynchronously
        # Note: order is not guaranteed but that doesn't matter since we wait
        # until all overlay frames are generated
        pool.apply_async(generate_overlay_frame, [i, velocity, time_point])
    pool.close()
    pool.join()

    # Convert all individual overlay frames to a video
    fps = 30
    frame_name_format = 'temp/speed%d.png'
    output_overlay_path = 'temp/speed_overlay.mp4'
    convert_overlay_to_video(frame_name_format, output_overlay_path, fps)

    # Overlay video onto input video
    overlay_video_path = 'temp/speed_overlay.mp4'
    output_video_path = 'test_speed.mp4'
    overlay_x_pos = 25
    overlay_y_pos = 25

    overlay_video(input_video, overlay_video_path, output_video_path, overlay_x_pos, overlay_y_pos)

    end = time.time()

    print('total time (s) = ' + str(end-start))
    print('fps = ' + str(len(time_points)/(end-start)))
