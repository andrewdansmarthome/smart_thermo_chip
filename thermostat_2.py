import RPi.GPIO as GPIO
import time, threading, requests, json
from env.secrets import ENV_IP, ENV_LOCATION_ID

GPIO.setmode(GPIO.BCM)

# ~~~~~~~~ PIN SETUP ~~~~~~~~
global furnacePin, tempPin, ioTestPin, runTestPin
furnacePin = 17 # pin 11 WARNING: CREATES 'PIN IN USE' WARNING
tempPin = 27 # pin 13
ioTestPin = 26 # pin 37
runTestPin = 16 # pin 36

GPIO.setup(furnacePin, GPIO.OUT)
GPIO.setup(tempPin, GPIO.IN)
GPIO.setup(ioTestPin, GPIO.IN)
GPIO.setup(runTestPin, GPIO.IN)

# ~~~~~~~~ INIT VARIABLES ~~~~~~~~~
global processDelay, furnaceOn, previousTime, running
processDelay = 300 # in seconds
furnaceOn = False
previousTime = time.time()
running = True

# ~~~~~~~~ API URLS ~~~~~~~~~~~~
global urlRoot, urlConfig, urlTempData
urlRoot = ENV_IP + '/api/thermostat'
urlConfig = urlRoot + '/config/1'
urlTempData = urlRoot + '/temperature'

# ~~~~~~~~ CONFIG VARIABLES ~~~~~~~~~
global config
config = dict(
  id = 1,
  transmitDelay = 300, # server send delay (in seconds)
  targetTemp = 70, # current target temperature (degrees farenheight)
  nextScheduledTime = 0, # time since epoch for next scheduled action (in seconds)
  nextScheduledTemp = 68 # scheduled temp (deg F)
)

# ~~~~~ TEST VARIABLES ~~~~~~
global testTemp
testTemp = dict(
  temperature = 70,
  serializedValue = 1,
  time = int(time.time()),
  targetTemperature = 72,
  locationId = ENV_LOCATION_ID
)

def initializeApp():
  # Read from default config file and initialize config dictionary
  print('all functions must have actual code in them')
  global config
  res = requests.get(urlConfig + config['id'])
  data = res.json()
  print('data', data)
  config = data['config']

def updateConfig():
  global config
  initURL = urlConfig
  res = requests.get(url = urlConfig)
  data = res.json()
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

def ioTestToggle(event):
  print('event: ', event)
  furnaceControl(not furnaceOn)

def ioRunToggle():
  global config
  config['running'] = False

# Initialize listener on ioTestPin
GPIO.add_event_detect(ioTestPin, GPIO.FALLING, callback=ioTestToggle, bouncetime=200)
GPIO.add_event_detect(runTestPin, GPIO.RISING, callback=ioRunToggle, bouncetime=200)

sendConfig()

# Run scheduling process
while running:
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
  print('ioTestPin: ', GPIO.input(ioTestPin), 'runTestPin: ', GPIO.input(runTestPin), 'cycleTime: ', cycleTime)
  time.sleep(5)
