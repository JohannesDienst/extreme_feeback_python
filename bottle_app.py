#!/usr/bin/python


# setup gpio
import time
import RPi.GPIO as GPIO

# RPi.GPIO Layout (PIN-Numbers)
GPIO.setmode(GPIO.BOARD)

# Pin 11 (GPIO 17) Output
GPIO.setup(11, GPIO.OUT)
GPIO.output(11, GPIO.LOW)

# Pin 13 (GPIO 27) Output
GPIO.setup(13, GPIO.OUT)
GPIO.output(13, GPIO.LOW)

GPIO.output(11, GPIO.LOW)
GPIO.output(13, GPIO.HIGH)

#setup modules
import json
builds = json.load(open("builds.json"))

def evaluateStatus(module=None, status=None):
    print "Evaluate status: " + str(builds)
    if module != None and status != None:
        builds[module] = status
    print builds

    status = "stable"
    for key, value in builds.iteritems():
       print( str(key) + " " + str(value))
       if value != "stable":
           print("Unstable: " + str(key))
           status = "unstable"
           return status
    return status

def setGPIO(status):
    if status == "stable":
        print("Green")
        GPIO.output(11, GPIO.LOW)
        GPIO.output(13, GPIO.HIGH)
    else:
        print("Red")
        GPIO.output(11, GPIO.HIGH)
        GPIO.output(13, GPIO.LOW)

status = evaluateStatus()
print("Starting with status: " + str(status))
setGPIO(status)

# setup bottle
from bottle import route, request, run

@route('/build')
def status():
    module = request.query.module
    status = request.query.status

    if status == "success":
        status = "stable"
    else:
        status = "unstable"

    print("module: " + module + " has status: " + str(status))

    status = evaluateStatus(module, status)
    setGPIO(status)

    return str(module) + " " + str(status)

run(host='192.168.0.14', port=7073, reloader=True,  debug=True)
