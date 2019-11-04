from GPXOverlay import overlay

def main():
    speed_overlay = overlay.Overlay('./examples/sample-data.gpx', './examples/video.mp4')
    speed_overlay.generate_overlay_frames()
    speed_overlay.convert_overlay_to_video()
    speed_overlay.overlay_video()

main()
