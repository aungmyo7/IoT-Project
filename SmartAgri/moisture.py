#!/usr/bin/python

# Start by importing the libraries we want to use
import sys
import RPi.GPIO as GPIO # This is the GPIO library we need to use the GPIO pins on the Raspberry Pi
import smbus # This is to use I2C_device
from I2C_device import * # This is to use LED display
from Lcd import * # This is to use LED display
import time # This is the time library, we need this so we can use the sleep function
import datetime
import sqlite3

# This is the message that will be sent when NO moisture is detected
message_need_water = "Warning, plant needs water! Water pump will turn on automatically."

# This is the message that will be sent when moisture IS detected again
message_noneed_water = "Plant has enough water now and water pump is turned off."

# Save data to DB
def savedata(plantId, moistureLevel):
        data = (
          {'Id':plantId, 'MoistureLevel':moistureLevel, 'RecordedDate':datetime.datetime.now()}
       )

        connection = None
        try:
            connection = sqlite3.connect('mydatabase.db')
            with connection:
                cursor = connection.cursor()    
                cursor.execute("INSERT INTO PlantData VALUES (:Id,:MoistureLevel,:RecordedDate)", data)
        except sqlite3.Error, e:
            print "Error %s:" % e.args[0]
            sys.exit(1)
        finally:
            if connection:
                connection.close()

# This is the callback function. It will be called every time there is a change on the specified GPIO channel. In this example we are using 17.
def callback(channel):  
	if GPIO.input(channel):
		print "LED off"
		lcd = Lcd()
                lcd.clear()
                lcd.display_string(message_need_water,1)
                savedata(1,"Need water")
	else:
		print "LED on"
		lcd = Lcd()
                lcd.clear()
                lcd.display_string(message_noneed_water,1)
                savedata(1,"No need water")

# Set our GPIO numbering to BCM
GPIO.setmode(GPIO.BCM)

# Define the GPIO pin that we have our digital output from our sensor connected to
channel = 17
# Set the GPIO pin to an input
GPIO.setup(channel, GPIO.IN)

# This line tells our script to keep an eye on our gpio pin and let us know when the pin goes HIGH or LOW
GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=300)
# This line asigns a function to the GPIO pin so that when the above line tells us there is a change on the pin, run this function
GPIO.add_event_callback(channel, callback)

# This is an infinte loop to keep our script running
while True:
	# This line simply tells our script to wait 0.1 of a second, this is so the script doesnt hog all of the CPU
	time.sleep(0.1)
