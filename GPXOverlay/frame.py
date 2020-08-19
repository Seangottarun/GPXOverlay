"""This module generates individual frames used to generate the output video
"""
import imgkit
import jinja2
import matplotlib.pyplot as plt
import math
import numpy as np

# relative project paths to HTML and CSS templates
SPEED_HTML = "./GPXOverlay/templates/speed_template.html"
SPEED_CSS = './GPXOverlay/static/speed_template.css'

ELEVATION_HTML = "./GPXOverlay/templates/elevation_template.html"
ELEVATION_CSS = './GPXOverlay/static/elevation_template.css'

def generate_png(speed, time, id):
    """Generates a single frame as a png using the instantaneous speed and time

    Args:
        speed (float): Instantaneous speed
        time (float): Instantaneous time
        id (int): Unique id number for this frame

    Returns: None

    """
    # Load template using jinja2
    templateLoader = jinja2.FileSystemLoader(searchpath="./")
    templateEnv = jinja2.Environment(loader=templateLoader)
    template = templateEnv.get_template(SPEED_HTML)
    # Modify template with instantaneous speed and time
    output_from_parsed_template = template.render(speed=speed,time=time)

    # Save modified template in temporary HTML file
    with open("temp/updated_speed.html", "w+") as new_html_file:
        new_html_file.write(output_from_parsed_template)

    # Use imgkit to generate png from temporary HTML file
    options = {'quiet': '', 'transparent': '', 'width': 500, "crop-w":500, 'disable-smart-width': ''} # turn off intermediate status notifications
    imgkit.from_file('temp/updated_speed.html', f'temp/speed{id}.png', options=options, css=SPEED_CSS) # output image to location w/ fstring


def graph_elevation(time, elevation, size, avg, y_min, y_max):
    """Generates a single frame using a subset of the time and elevation data.

    The generated graph displays a subset of the time and elevation data up to a
    a certain time. This allows the data to be plotted as an animation when the
    frames are combined into a video. The max, min, and avg elevation values
    obtained over the entire array are plotted using arrays to force matplotlib
    to show the whole graph.

    Args:
        time (ndarray): Subset of time array to be plotted
        elevation (ndarray): Subset of elevation array to be plotted
        size (int): Size of full elevation array
        avg (float): Average of full elevation array
        y_min (float): Minimum of full elevation array
        y_max (float): Maximum of full elevation array

    Returns: None

    """

    # Initialize arrays for minimum, average, and maximum elevation values
    x = np.linspace(0,size-1,size)
    avg = avg * np.ones(size)
    y_min_array = y_max * np.ones(size)
    y_max_array = y_min * np.ones(size)

    fig, ax = plt.subplots()
    ax.plot(x, avg, color='#D430AB')
    ax.plot(time,elevation, color='#eafff5')
    ax.plot(x, y_max_array, color='#13DEF2')
    ax.plot(x, y_min_array, color='#0B0E6A')

    ax.set_ylabel('Elevation [m]', color='#ffffff')
    ax.set_xlabel('Time [s]', color='#ffffff')
    ax.tick_params(labelcolor='#ffffff')

    ax.spines['top'].set_color('#cdcdcd')
    ax.spines['bottom'].set_color('#cdcdcd')
    ax.spines['left'].set_color('#cdcdcd')
    ax.spines['right'].set_color('#cdcdcd')

    ax.tick_params(axis='x', colors='#ffffff')
    ax.tick_params(axis='y', colors='#ffffff')

    fig.savefig('temp/elevation.png', transparent=True)
    plt.close(fig) # Need to close figure to save memory

def generate_elevation_frame(id):
    """Generates a single frame as a png using the temporary elevation graph

    Args:
        id (int): Unique identifier for the generated elevation frame

    Returns: None

    """
    # Use imgkit to generate png from HTML template
    options = {'quiet': '', 'transparent': '', 'width':775, 'height': 775, "crop-w":775, 'disable-smart-width': ''} # turn off intermediate status notifications
    imgkit.from_file(ELEVATION_HTML, f'temp/elevation{id}.png', options=options) # output image to location w/ fstring
