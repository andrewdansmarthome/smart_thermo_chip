import RPi.GPIO as GPIO
import time, threading, requests, json, sys
from env.env import ENV_API_URL, ENV_LOCATION_ID
from api_urls import apiTemperature

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
    tempPin = 27, # see pin-setup
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
  
  def sendTemp(self, temp):
    # Send temp data to server
    print('sendTemp has fired!')
    requests.post(apiTemperature, json=temp)
  
  def convertTemp(self, serializedTemp):
    # Convert temperature data from ADC value to deg Farenheight
    print('convertTemp fired!')
  
  def readTemp(self):
    curVoltage = GPIO.input(self.tempPin)
    curTime = int(time.time())
    curTemp = self.convertTemp(curVoltage)
    self.tempStore[curTime] = 

