import os
import multiprocessing
import time

from GPXOverlay import analysis
from GPXOverlay.overlay import *
from GPXOverlay import frame

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
    gpx_file = 'sample-data-short.gpx'
    data = analysis.Analysis(gpx_file)
    time_points = data.time_data
    velocities = data.velocity_data

    if not os.path.exists('temp'):
        os.makedirs('temp')

    start = time.time()

    # Create a pool with same number of worker processes as number of cpu cores
    pool = multiprocessing.Pool()

    for i, (velocity, time_point) in enumerate(zip(velocities, time_points)):
        # Generate each overlay frame asynchronously
        # Note: order is not guaranteed but that doesn't matter since we wait
        # until all overlay frames are generated
        pool.apply_async(generate_overlay_frame, [i, velocity, time_point])
    pool.close()
    pool.join()

    end = time.time()

    # Convert all individual overlay frames to a video
    fps = 30
    frame_name_format = 'temp/speed%d.png'
    output_overlay_path = 'temp/speed_overlay.mp4'
    convert_overlay_to_video(frame_name_format, output_overlay_path, fps)

    # Overlay video onto input video
    input_video = 'video.mp4'
    overlay_video_path = 'temp/speed_overlay.mp4'
    output_video_path = 'test_speed.mp4'
    overlay_x_pos = 25
    overlay_y_pos = 25

    overlay_video(input_video, overlay_video_path, output_video_path, overlay_x_pos, overlay_y_pos)

    print('total time (s) = ' + str(end-start))
    print('fps = ' + str(len(time_points)/(end-start)))
