import datetime
import sqlite3
import sys

from django.conf import settings
from django.template.loader import get_template
from django.template import Context

from django.http import HttpResponse
from django.http import JsonResponse

from Lcd import *
from Relay import *

def home(request):
    dt = datetime.datetime.now()
    html = '''
    <html><body><h1>Welcome from Smart Agriculture</h1>
    <p>Time now: %s.</p>
    <br/>
    <a href="/dashboard">Dashboard</a>
    <a href="/pumpon">pumpon</a>
    <a href="/pumpoff">pumpff</a>
    </body></html>''' % (dt,)
    return HttpResponse(html)

def dashboard(request):
    connection = None
    data = dict()
    data['title'] = "Plants Irrigation Info"
    data['static']=settings.STATIC_URL
    try:
        connection = sqlite3.connect('/home/pi/SmartAgri/mydatabase.db')
        with connection:
            cursor = connection.cursor()
            cursor.execute("SELECT Id,MoistureLevel,RecordedDate FROM PlantData")
            data['PlantData'] = cursor.fetchall()
    except sqlite3.Error, e:
        print "Error %s:" % e.args[0]
        sys.exit(1)
    finally:
        if connection:
            connection.close()
    html = get_template('dashboard.html').render(Context(data))
    return HttpResponse(html)

def pumpswitchOn(request):
	lcd = Lcd()
	lcd.clear()
	lcd.display_string("pump on",1)
	relay = Relay()
	relay.switch(3,1)
	response_mesage={
		"result":"pump is on"
	}
	return JsonResponse(response_mesage)

def pumpswitchOff(request):
	lcd = Lcd()
	lcd.clear()
	lcd.display_string("pump off",1)
	relay = Relay()
	relay.switch(3,0)
	response_mesage={
		"result":"pump is off"
	}
	return JsonResponse(response_mesage)

def latestSensorData(request):
    connection = None
    data = dict()
    data['title'] = "Plants Irrigation Info"
    try:
        connection = sqlite3.connect('/home/pi/SmartAgri/mydatabase.db')
        with connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM PlantData ORDER BY RecordedDate DESC LIMIT 1")
            data['PlantData'] = cursor.fetchall()
            jsonResult={
                "moisturelevel":100
            }
    except sqlite3.Error, e:
        print "Error %s:" % e.args[0]
        sys.exit(1)
    finally:
        if connection:
            connection.close()

    return JsonResponse(jsonResult)
