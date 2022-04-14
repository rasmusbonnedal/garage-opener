#!/usr/bin/env python3

import RPi.GPIO as GPIO
import distance
import discordmsg
from time import sleep
from datetime import datetime
from threading import Thread, current_thread
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
import uuid

def nowstring():
    return datetime.now().strftime('[%Y-%m-%d %H:%M:%S] ')

def log(msg):
    with open('garage.log', 'at') as file:
        t = nowstring() + msg
        print(t, file=file)
        print(t)

def is_garage_open():
    return int(round(distance.distance(), 0)) < 20

def garage_watchdog():
    log(f'Starting watchdog thread')
    WARN_PERIOD = 30 * 60 # seconds
    garage_open = is_garage_open()
    open_since = datetime.now()
    last_warning = datetime.now()
    
    while True:
        new_state = is_garage_open()
        curr_time = datetime.now()

        if not garage_open and new_state:
            open_since = curr_time
            last_warning = curr_time

        if garage_open and new_state:
            if (curr_time - last_warning).seconds >= WARN_PERIOD:
                last_warning = curr_time
                open_time = (curr_time - open_since).seconds // 60
                open_since_str = open_since.strftime('%Y-%m-%d %H:%M')
                msg = f'Garage has been open for {open_time} minutes, since {open_since_str}'
                log(msg)
                discordmsg.send_message(msg)

        garage_open = new_state
        sleep(20)

def trigger_garage_button():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    pin = 22
    GPIO.setup(pin, GPIO.OUT)
    log('GPIO ON')
    GPIO.output(pin, True)
    sleep(1)
    log('GPIO OFF')
    GPIO.output(pin, False)

app = Flask(__name__)

@app.route('/garage', methods=['GET', 'POST'])
def garage():
    ipstring = request.remote_addr
    if request.method == 'POST':
        log('POST ' + ipstring)
        req_nonce = request.form.get('nonce')
        if app.nonce == req_nonce:
            app.nonce = None
            trigger_garage_button()
            discordmsg.send_message('Garage button pressed by ' + ipstring + ' ' + nowstring())
        else:
            log(f'Error in nonce {app.nonce}, {req_nonce}')
        return redirect(url_for('garage'))
    else:
        log('GET ' + ipstring)
        dist = int(round(distance.distance(), 0))
        garage_open = dist < 20
        app.nonce = uuid.uuid4().hex
        return render_template('garage.html', distance=dist, garage_open=garage_open, nonce=app.nonce)

@app.route('/apple-touch-icon.png')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon-180.png')
    
if __name__ == '__main__':
    t = Thread(target=garage_watchdog, daemon=True)
    t.start()
    app.run(debug=False, host='0.0.0.0')
