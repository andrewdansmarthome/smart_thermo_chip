import RPi.GPIO as GPIO
import time, threading, requests, json, sys
from env.env import ENV_API_URL, ENV_LOCATION_ID
from board_setup import BoardSetup

# ~~~~~~~~ API URLS ~~~~~~~~~~~~
urlTemperature = ENV_API_URL + '/thermostat/temperature'

# ~~~~~ TEST VARIABLES ~~~~~~
testTemp = dict(
  temperature = 70,
  serializedTemp = 1,
  time = int(time.time()),
  targetTemperature = 72,
  locationId = ENV_LOCATION_ID
)

# ~~~~~~~~ INIT VARIABLES ~~~~~~~~~
initTemp = dict(
    # default temp setup
    tempPin = 27,
    temperature = 0,
    serializedTemp = 0,
    targetTemperature = 70,
    serialConversionFactor = 213/1024 # 70 deg is 213/1024
)

class Temperature:
  def __init__(self, temp):
    self.tempPin = temp['tempPin']
    self.temperature = temp['temperature']
    self.serializedTemp = temp['serializedTemp']
    self.targetTemperature = temp['temperaute']
    self.serialConversionFactor = temp['serialConversionFactor']
  
  def readTemp(self):
    self.serializedTemp = GPIO.input(self.tempPin)
    return self.convertTemp(self.serializedTemp)

  def sendTemp(self, temp):
    print('sendTemp has fired!')
    # Send temp data to server
    res = requests.post(urlTemperature, json = temp)
    print('res: ', res)

  def convertTemp(self, serializedTemp):
    # Convert temperature data from ADC value to deg Farenheight
    temp = serializedTemp * self.serialConversionFactor
    print('Converted Temp: ', temp)
    return temp
