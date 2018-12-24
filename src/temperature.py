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
    tempPin = board,
    temperature = 0,
    serializedTemp = 0,
    targetTemperature = 70,
    serialToVoltageFactor = 5000 / 1024, # Convert serial to voltage
    voltageToTempFactor = 10, # 10 mV/degC
    voltageOffset = 500 # tmp36 offset 500mV
)

class Temperature:
  def __init__(self, tempData):
    self.tempPin = tempData['tempPin']
    self.temp = tempData['temperature']
    self.serializedTemp = tempData['serializedTemp']
    self.targetTemp = tempData['targetTemperaute']
    self.serialToVoltageFactor = tempData['serialToVoltageFactor']
    self.voltageToTempFactor = tempData['voltageToTempFactor']
    self.voltageOffset = tempData['voltageOffset']
    self.tempStore = dict()

  def readTemp(self):
    self.serializedTemp = GPIO.input(self.tempPin)
    self.temp = self.convertTemp(self.serializedTemp),
    return self.temp

  def sendTemp(self):
    print('sendTemp has fired!')
    # Build temp payload
    # Send temp data to server
    res = requests.post(urlTemperature, json = self.tempStore)
    if res.status_code == 204:
      self.tempStore = dict()
    else:
      print('There was an error sending the bundled Temp data. Response code: ', res.status_code)
    print('res: ', res)

  def convertTemp(self, serializedTemp):
    # Convert temperature data from ADC value to deg Farenheight
    temp = ( serializedTemp * self.serialToVoltageFactor - self.voltageOffset ) / self.voltageToTempFactor
    print('Converted Temp: ', temp)
    return temp
  
  def storeTemperature(self, temp):
    self.tempStore[round(time.time()*1000)] = temp
