#!/usr/bin/python

#rax-rpi-lights - Christophe Delcourt <cd.delcourt@gmail.com>

# Some references to the LED's

# Row 1 Red		= pin 13
# Row 1 Amber		= pin 12
# Row 1 Green		= pin 7

# Row 2 Red		= pin 18
# Row 2 Amber		= pin 16
# Row 2 Green		= pin 15

from raxmon_cli.common import run_action
from time import sleep
import re
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD) #Set the board mode. BCM Pinouts are different, hence BOARD

leds = [13, 12, 7, 18, 16, 15] #Set up the GPIO pins to be used

for n in leds: #Reset all LEDs
	GPIO.setup(n, GPIO.OUT)
	GPIO.output(n, False)

def checkAlerts():

	OPTIONS = None
	REQUIRED_OPTIONS = None

	def callback(driver, options, args, callback):
		result = str(driver.ex_views_overview(ex_next_marker=options.marker))

		red = len(re.findall("CRITICAL", result))
		orange = len(re.findall("WARNING", result))
		green = len(re.findall("OK", result))
		print("Red:", red, "Orange:", orange, "Green:", green)

		for n in leds:
			GPIO.output(n, False)
		if red > 0:  #If something is wrong, light up the red light
			GPIO.output(13,GPIO.HIGH)

		if red > 5:  #If something is *really* wrong, flash the red light to grab my attention!
			GPIO.output(13,GPIO.LOW)
			sleep(0.2)
			GPIO.output(13,GPIO.HIGH)
			sleep(0.2)			
			GPIO.output(13,GPIO.LOW)
			sleep(0.2)
			GPIO.output(13,GPIO.HIGH)

		if orange > 0:
			GPIO.output(12,GPIO.HIGH)

		if green > 0: #If any OK is returned, turn on the green light
			GPIO.output(7,GPIO.HIGH)

	run_action(OPTIONS, REQUIRED_OPTIONS, 'views', 'overview', callback)

count = 0
while True:
	count += 1
	sleep (5)
	checkAlerts()