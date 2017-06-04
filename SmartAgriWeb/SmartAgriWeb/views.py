import datetime
import sqlite3
import sys
 
from django.template.loader import get_template
from django.template import Context
 
from django.http import HttpResponse
 
def home(request):
    dt = datetime.datetime.now()
    html = '''
    <html><body><h1>Welcome from Smart Agriculture</h1>
    <p>Time now: %s.</p>
    <br/>
    <a href="http://localhost:8080/dashboard">Dashboard</a>
    </body></html>''' % (dt,)
    return HttpResponse(html)

def dashboard(request):
    connection = None
    data = dict()
    data['title'] = "Plants Irrigation Info"
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
