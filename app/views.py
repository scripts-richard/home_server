import json
import requests

from app import app
from flask import render_template, request
from flask_wtf import FlaskForm

from hue import Hue, xy_to_rgb
from server_settings import get_ip_address, NETDATA_PORT, PLEX_PORT, ROUTER_ADDRESS, WEATHER_IP


@app.route('/')
def index():
    ip = get_ip_address('eth0')
    http = 'http://'
    netdata_address = http + ip + NETDATA_PORT
    plex_address = http + ip + PLEX_PORT + '/manage/index.html'
    pihole_address = http + ip + '/admin'
    router_address = http + ROUTER_ADDRESS
    return render_template('index.html',
                           netdata_address=netdata_address,
                           plex_address=plex_address,
                           pihole_address=pihole_address,
                           router_address=router_address)


@app.route('/hue_control', methods=['GET', 'POST'])
def hue_control():
    myhue = Hue()
    colors = {}
    form = FlaskForm()
    on = False
    count = len(myhue.lights)

    for light in myhue.lights:
        x = myhue.lights[light]['state']['xy'][0]
        y = myhue.lights[light]['state']['xy'][1]
        brightness = myhue.lights[light]['state']['bri'] / 254

        if x > 0  and y > 0:
            r, g, b = xy_to_rgb(x, y, brightness)
        else:
            r, g, b = 0, 0, 0

        colors[light] = {'r': r, 'g': g, 'b': b}
        if myhue.lights[light]['state']['on']:
            on = True

    return render_template('hue_control.html',
                           title='Hue Control',
                           lights=myhue.lights,
                           colors=colors,
                           form=form,
                           on=on,
                           count=count)


@app.route('/weather')
def weather():
    url = 'http://' + WEATHER_IP
    data = json.loads(requests.get(url).content.decode())
    temperature = data['temperature']
    humidity = data['humidity']
    return render_template('weather.html',
                           temperature=temperature,
                           humidity=humidity)


@app.route('/toggle/<light>', methods=['GET', 'POST'])
def toggle(light):
    myhue = Hue()
    myhue.toggle_light(light)
    return json.dumps({'success': True})


@app.route('/toggle_all', methods=['GET', 'POST'])
def toggle_all():
    myhue = Hue()
    myhue.toggle_lights()
    return json.dumps({'success': True})


@app.route('/apply_changes', methods=['POST'])
def apply_changes():
    data = request.form
    colors = {}
    myhue = Hue()
    for key, val in data.items():
        if key != 'csrf_token':
            light_id = key[1]
            color = key[0]
            if light_id not in colors:
                colors[light_id] = {}
            colors[light_id][color] = val
    myhue.update_via_rgb(colors)
    return json.dumps({'success': True})


@app.route('/test', methods=['POST'])
def test_post():
    data = request.form
    print(data)
    return json.dumps({'success': True})


@app.route('/print/<line>')
def print_line(line):
    print(line)
    return json.dumps({'success': True})
