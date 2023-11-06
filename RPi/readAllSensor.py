import adafruit_dht
import paho.mqtt.client as mqtt
import json, geocoder
import time
from lightsensorRead import readLight
import mh_z19
import board, geocoder
# from sds011reader import SDS011Reader
import simple_sds011
from mqtthelper import publish



#get lat and long
location = geocoder.ip('me')
if location.ok:
    latitude = location.latlng[0]
    longitude = location.latlng[1]
else:
    latitude = 0.0
    longitude = 0.0


#read light sensor
try:
  lightlevel = round(readLight(),2)
except:
  lightlevel = -1.0
#light sensor value is -1 if there is sensor error

#read CO2 level
try:
    co2Sensor = mh_z19.read_all()
    co2Sensor = mh_z19.read_all()
    co2 = co2Sensor['co2']
    temperatureco2 = co2Sensor['temperature']
except:
  co2 = -1
  temperatureco2 = -1

#Read DHT11
try:
  dhtDevice = adafruit_dht.DHT11(board.D17)
  humidity = dhtDevice.humidity
  temperature = dhtDevice.temperature
except:
  humidity = -1
  temperature = -1

#Read PM2.5 and PM10    
# try:
# AQIsensor = SDS011Reader()
# PM = AQIsensor.readValue()
pm = simple_sds011.SDS011('/dev/ttyUSB0')
PM = pm.query()
# except:
    # PM = [-1, -1]

data = {
  'lightlevel':lightlevel,
  'co2':co2,
  'temperatureco2':temperatureco2,
  'pm2_5':PM['value']['pm2.5'],
  'pm10':PM['value']['pm10.0'],
  'temperature': temperature,
  'humidity': humidity,
  'fetchtime': int(time.time()),
  'lat':latitude,
  'lon':longitude
}
print(data)
publish("JM/ALLSENSOR",data)
