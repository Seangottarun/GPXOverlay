from GPXOverlay import analysis
from GPXOverlay import overlay
import matplotlib.pyplot as plt
import numpy as np
import imgkit

def main():
    # load GPX file into an Analysis object and graph data
    data = analysis.Analysis('sample-data-short.gpx')
    ele = data.elevation_data
    fig, ax = plt.subplots()
    ax.plot(ele, color='#2d89ef')
    ax.set_ylabel('Elevation [m]')
    ax.set_xlabel('Time [s]')
    ax.set_title("Elevation Profile")
    fig.savefig('elevation_profile.png')

main()
