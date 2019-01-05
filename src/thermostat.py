import RPi.GPIO as GPIO
import time, threading, requests, json, sys
from env.env import ENV_API_URL, ENV_LOCATION_ID
from config import Config, initConfig
from scheduler import Scheduler
from temperature import Temperature, initTemp
from pin_setup import PinSetup

pins = PinSetup()
config = Config(initConfig)
scheduler = Scheduler(config.chipId)
temperature = Temperature(initTemp)


# ~~~~~~~~ INIT VARIABLES ~~~~~~~~~
global furnaceOn, previousTime, running
furnaceOn = False
previousTime = time.time()
running = True

# ~~~~~~~~ API URL ~~~~~~~~~~~~
urlThermostat = ENV_API_URL + '/api/thermostat'

def ioRunToggle(self):
    config['running'] = False

def scheduler(curTime):
  global config
  if (curTime >= config['nextScheduledTime']):
    config['targetTemp'] = config['nextScheduledTemp']
    readSchedule(config['nextScheduledTime'])

def readSchedule(curTime):
  # Read schedule file and return nextScheduledTemp and nextScheduledTime
  print('readSchedule fired!')

class Thermostat:
  # def __init__(self):

  def run(self):
    # Initialize listener on ioTestPin
    GPIO.add_event_detect(ioTestPin, GPIO.FALLING, callback=ioTestToggle, bouncetime=200)
    GPIO.add_event_detect(runTestPin, GPIO.RISING, callback=ioRunToggle, bouncetime=200)
    sendConfig()
    # Run scheduling process
    while config['running']:
      global previousTime, config, ioTestPin, ioRunPin

      print(testTemp)

      temp = readTemp()
      curTime = time.time()
      cycleTime = curTime - previousTime

      # Run scheduler
      scheduler(cycleTime)

      # Send stored temperature data
      if (cycleTime > config['transmitDelay']):
        previousTime = time.time()
        sendTemp(testTemp)

      sendTemp(testTemp)
      print('ioTestPin: ', GPIO.input(ioTestPin), 'runTestPin: ',
            GPIO.input(runTestPin), 'cycleTime: ', cycleTime)
      time.sleep(5)
