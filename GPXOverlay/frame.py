import imgkit
import jinja2

SPEED_TEMPLATE_FILE = "speed_template.html"
css = './GPXOverlay/static/speed_template.css'

def generate_png(speed, time, id):
    templateLoader = jinja2.FileSystemLoader(searchpath="./GPXOverlay/templates")
    templateEnv = jinja2.Environment(loader=templateLoader)
    template = templateEnv.get_template(SPEED_TEMPLATE_FILE)
    output_from_parsed_template = template.render(speed=speed,time=time)

    # to save the results
    with open("updated_speed.html", "w") as new_html_file:
        new_html_file.write(output_from_parsed_template)

    options = {'quiet': '', 'transparent': '', 'width': 500, "crop-w":500, 'disable-smart-width': ''} # turn off intermediate status notifications
    # css = speed.css
    imgkit.from_file('updated_speed.html', f'temp/out{id}.png', options=options, css=css) # output image to location w/ fstring
