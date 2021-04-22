#!/usr/bin/env python3

import RPi.GPIO as GPIO
import distance
import discordmsg
from time import sleep
from datetime import datetime
from threading import Thread
from flask import Flask, render_template, request, redirect, url_for

def is_garage_open():
    return int(round(distance.distance(), 0)) < 20

def garage_watchdog():
    print('Starting watchdog thread')
    WARN_PERIOD = 120 # seconds
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
                open_time = (curr_time - open_since)
                msg = f'Garage has been open for {open_time}, since {open_since}'
                print(msg)
                discordmsg.send_message(msg)

        garage_open = new_state
        sleep(60)

def trigger_garage_button():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    pin = 22
    GPIO.setup(pin, GPIO.OUT)
    print('ON')
    GPIO.output(pin, True)
    sleep(1)
    print('OFF')
    GPIO.output(pin, False)

app = Flask(__name__)

@app.route('/garage', methods=['GET', 'POST'])
def garage():
    if request.method == 'POST':
        trigger_garage_button()
        discordmsg.send_message('Garage button pressed')
        return redirect(url_for('garage'))
    else:
        dist = int(round(distance.distance(), 0))
        garage_open = dist < 20
        print(garage_open)
        return render_template('garage.html', distance=dist, garage_open=garage_open)

if __name__ == '__main__':
    t = Thread(target=garage_watchdog, daemon=True)
    t.start()
    app.run(debug=True, host='0.0.0.0')

