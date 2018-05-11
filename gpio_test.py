#!/usr/bin/env python

import RPi.GPIO as GPIO
from time import sleep
from flask import Flask, render_template, request, redirect, url_for

def trigger_garage_button():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    pin = 22
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, True)
    sleep(0.5)
    GPIO.output(pin, False)

app = Flask(__name__)

@app.route('/garage', methods=['GET', 'POST'])
def garage():
    if request.method == 'POST':
        trigger_garage_button()
        return redirect(url_for('garage'))
    else:
        return render_template('garage.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

