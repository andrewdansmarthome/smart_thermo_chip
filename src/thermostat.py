import RPi.GPIO as GPIO
import time, threading, requests, json, sys
from env.env import ENV_API_URL, ENV_LOCATION_ID
from config import Config, initConfig
from scheduler import Scheduler
from temperature import Temperature
from board_setup import BoardSetup

GPIO.setmode(GPIO.BCM)

boardSetup = BoardSetup()
config = Config(initConfig)
scheduler = Scheduler(config.chipId)

# ~~~~~~~~ INIT VARIABLES ~~~~~~~~~
global furnaceOn, previousTime, running
furnaceOn = False
previousTime = time.time()
running = True

# ~~~~~~~~ API URL ~~~~~~~~~~~~
urlThermostat = ENV_API_URL + '/api/thermostat'

def initializeApp():
  # Read from default config file and initialize config dictionary
  print('all functions must have actual code in them')
  global config
  res = requests.get(urlConfig + config['id'])
  data = res.json()
  print('data', data)
  config = data['config']

def furnaceControl(turnFurnaceOn = furnaceOn):
  global furnaceOn
  if (turnFurnaceOn):
    GPIO.output(furnacePin, GPIO.HIGH)
    furnaceOn = True
  else:
    GPIO.output(furnacePin, GPIO.LOW)
    furnaceOn = False

def readTemp():
  curVoltage = GPIO.input(tempPin)
  return convertTemp(curVoltage)

def sendTemp(temp):
  # Send temp data to server
  print('sendTemp has fired!')
  requests.post(urlTempData, json = temp)

def convertTemp(serializedTemp):
  # Convert temperature data from ADC value to deg Farenheight
  print('convertTemp fired!')

def readConfig():
  # readConfig from static file
  print('readConfig fired!')

def writeConfig():
  # write config to static file
  print('writeConfig fired!')

def sendConfig():
	# updating config in db
  requests.post(urlConfig, json=config)

def scheduler(curTime):
  global config
  if (curTime >= config['nextScheduledTime']):
    config['targetTemp'] = config['nextScheduledTemp']
    readSchedule(config['nextScheduledTime'])

def readSchedule(curTime):
  # Read schedule file and return nextScheduledTemp and nextScheduledTime
  print('readSchedule fired!')

def ioTestToggle():
  furnaceControl(not furnaceOn)

def ioRunToggle():
  global config
  config['running'] = False

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
