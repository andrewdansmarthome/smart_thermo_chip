import RPi.GPIO as GPIO
import time, requests, json, sys
from env_setup import ENV_LOCATION_ID
from api_urls import apiTemperature
import Adafruit_MCP3008 as ADC

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
  def __init__(self, tempData, pins):
    self.tempPin = tempData['tempPin']
    self.temp = tempData['temperature']
    self.serializedTemp = tempData['serializedTemp']
    self.serialToVoltageFactor = tempData['serialToVoltageFactor']
    self.voltageToTempFactor = tempData['voltageToTempFactor']
    self.voltageOffset = tempData['voltageOffset']
    self.tempStore = dict()
    self.mcp = ADC.MCP3008(clk=pins.clk, cs=pins.cs, miso=pins.miso, mosi=pins.mosi)
  
  def sendTemp(self):
    # Send temp data to server
    print('sendTemp has fired!')
    requests.post(apiTemperature, json=self.tempStore)
  
  def convertTemp(self, serializedTemp):
    # Convert temperature data from ADC value to deg Farenheight
    print('convertTemp fired!')
  
  def readTemp(self):
    values = [0]*8
    for i in range(8):
      values[i] = self.mcp.read_adc(i)
    print(' | {0:>4}  | {1:>4}  | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4}  | {7:>4} |'.format(*values))

    return values[0]

