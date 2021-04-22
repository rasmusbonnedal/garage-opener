#!/usr/bin/env python

import RPi.GPIO as GPIO
import distance
from time import sleep
from flask import Flask, render_template, request, redirect, url_for

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
        return redirect(url_for('garage'))
    else:
        dist = int(round(distance.distance(), 0))
        garage_open = dist < 200
        print(garage_open)
        return render_template('garage.html', distance=dist, garage_open=garage_open)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

