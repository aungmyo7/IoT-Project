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
from Board import *

# This is the message that will be sent when NO moisture is detected
pumpStatus = "OFF"

# Save data to DB
def savedata(plantId, moistureLevel, pumpStatus):
        data = (
          {'Id':plantId, 'MoistureLevel':moistureLevel, 'PumpStatus':pumpStatus, 'RecordedDate':datetime.datetime.now()}
       )

        connection = None
        try:
            connection = sqlite3.connect('/home/pi/django/SmartAgri/mydatabase.db')
            with connection:
                cursor = connection.cursor()    
                cursor.execute("INSERT INTO PlantData VALUES (:Id,:MoistureLevel,:PumpStatus,:RecordedDate)", data)
        except sqlite3.Error, e:
            print "Error %s:" % e.args[0]
            sys.exit(1)
        finally:
            if connection:
                connection.close()

# This is the callback function. It will be called every time there is a change on the specified GPIO channel. In this example we are using 17.
def callback(moistureLevel):  
	if moistureLevel < 50:
		print "Water Pump On"
		lcd = Lcd()
                lcd.clear()
                pumpStatus = "ON"   
	else:
		print "Water Pump Off"
		lcd = Lcd()
                lcd.clear()
                pumpStatus = "OFF"
        lcd.display_string("Water Pump %s" % pumpStatus,1)
        latestMoistureLevel = getLatestMoistureLevel()
        print "Previous Moisture Level: %s " % latestMoistureLevel
        #print "moistureLevel %s " % moistureLevel

        latestMoistureLevel = int(latestMoistureLevel)
        moistureUp = latestMoistureLevel - moistureLevel
        moistureDown = moistureLevel - latestMoistureLevel

        print "moistureUp: %s " % moistureUp
        print "moistureDown: %s " % moistureDown
        
        if (moistureUp > 10) | (moistureDown > 10):
                savedata(1, moistureLevel, pumpStatus)


def getLatestMoistureLevel():
    connection = None
    try:
        connection = sqlite3.connect('/home/pi/django/SmartAgri/mydatabase.db')
        with connection:
            cursor = connection.cursor()
            cursor.execute("SELECT MoistureLevel FROM PlantData ORDER BY RecordedDate DESC LIMIT 1")
            moistureLevel = cursor.fetchone()[0]
    except sqlite3.Error, e:
        print "Error %s:" % e.args[0]
        sys.exit(1)
    finally:
        if connection:
            connection.close()
    return moistureLevel

# Set our GPIO numbering to BCM
# GPIO.setmode(GPIO.BCM)

# Define the GPIO pin that we have our digital output from our sensor connected to
# channel = 17
# Set the GPIO pin to an input
# GPIO.setup(channel, GPIO.IN)

# This line tells our script to keep an eye on our gpio pin and let us know when the pin goes HIGH or LOW
# GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=300)
# This line asigns a function to the GPIO pin so that when the above line tells us there is a change on the pin, run this function
# GPIO.add_event_callback(channel, callback)

# This is an infinte loop to keep our script running
#while True:
	# This line simply tells our script to wait 0.1 of a second, this is so the script doesnt hog all of the CPU
#	time.sleep(0.1)


def calculateMoistureLevel(moistureValue):
        moistureLevel = moistureValue - 70
        moistureLevel = (moistureLevel * 100) / 185
        moistureLevel = 100 - moistureLevel
        return moistureLevel

def main():
    board = Board()
    while (True):
        moistureValue = board.custom()
        moistureLevel = calculateMoistureLevel(moistureValue)
        print "%s: Moisture Level:%d percent" % (time.asctime(),
                               #board.control(),
                               #board.light(),
                               #board.temperature(),
                               moistureLevel)
        
        #board.output(board.control())
        callback(moistureLevel)
        time.sleep(1)
if __name__ == "__main__":
    main()
