#!/usr/bin/python


# setup gpio
import time
import RPi.GPIO as GPIO

# RPi.GPIO Layout verwenden (wie Pin-Nummern)
GPIO.setmode(GPIO.BOARD)

# Pin 6 (GPIO 17) auf Output setzen
GPIO.setup(11, GPIO.OUT)
GPIO.output(11, GPIO.LOW)

# Pin 7 (GPIO 27) auf Output setzen
GPIO.setup(13, GPIO.OUT)
GPIO.output(13, GPIO.LOW)

# setup bottle
from bottle import route, request, run

@route('/build')
def status():
    module = request.query.module
    status = request.query.status

    print("status: " + str(status))

    if status == "success":
        print("Red")
        GPIO.output(11, GPIO.LOW)
        GPIO.output(13, GPIO.HIGH)
    else:
        print("Green")
        GPIO.output(11, GPIO.HIGH)
        GPIO.output(13, GPIO.LOW)

    return str(module) + " " + str(status)

run(host='192.168.0.14', port=7073, reloader=True,  debug=True)
