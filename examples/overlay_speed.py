from GPXOverlay import overlay

def main():
    # load GPX file into an Overlay object and provide a path for output video
    speed_overlay = overlay.Overlay('sample-data-short.gpx', 'video.mp4')
    speed_overlay.generate_overlay_frames()
    speed_overlay.convert_overlay_to_video()
    speed_overlay.overlay_video()

main()
