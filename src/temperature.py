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
    targetTemperature = 70.0,
    serialToVoltageFactor = 5110 / 1024, # Convert serial to voltage
    voltageSource = 5110, # 10 mV/degC
    voltageOffset = 500 + 395 # tmp36 offset 500mV
)

class Temperature:
  def __init__(self, tempData, pins):
    self.tempPin = tempData['tempPin']
    self.temp = tempData['temperature']
    self.serializedTemp = tempData['serializedTemp']
    self.serialToVoltageFactor = tempData['serialToVoltageFactor']
    self.voltageSource = tempData['voltageSource']
    self.voltageOffset = tempData['voltageOffset']
    self.tempStore = []
    self.mcp = ADC.MCP3008(clk=pins.clk, cs=pins.cs, miso=pins.miso, mosi=pins.mosi)
  
  def sendTemp(self):
    # Send temp data to server
    res = requests.post(apiTemperature, json=self.tempStore)
    print('Temp response', res.json())
    self.tempStore = []
  
  def convertTemp(self, serializedTemp):
    # Convert temperature data from ADC value to deg Farenheight
    rawTemp = (((serializedTemp * self.serialToVoltageFactor) - self.voltageOffset) / 10) * 9/5 + 32
    curTemp = round(rawTemp, 2)
    return curTemp
  
  def readAndStoreTemp(self, curTime, targetTemp, chipId):
    curSerialTemp = self.readTemp(curTime)
    curTemp = self.convertTemp(curSerialTemp)
    tempDict = dict(
        temperature=curTemp,
        serializedValue=curSerialTemp,
        time=curTime,
        targetTemperature=targetTemp,
        chipId=chipId
    )
    self.tempStore.append(tempDict)
    print('temp: ', curTemp, 'serial: ', curSerialTemp)
    return curTemp

  def readTemp(self, curTime):
    values = [0]*8
    for i in range(8):
      values[i] = self.mcp.read_adc(i)
    return values[0]
