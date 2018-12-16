import RPi.GPIO as GPIO
import time, threading, requests

GPIO.setup(GPIO.BCM)

# ~~~~~~~~ PIN SETUP ~~~~~~~~
furnacePin = 17 # pin 11
tempPin = 27 # pin 13
ioTestPin = 26 # pin 37
runTestPin = 16 # pin 36

GPIO.setup(furnacePIn, GPIO.OUT)
GPIO.setup(tempPin, GPIO.IN)
GPIO.setup(ioTestPin, GPIO.IN)

# ~~~~~~~~ INIT VARIABLES ~~~~~~~~~
processDelay = 300 # in seconds
furnaceOn = False
previousTime = time.time()

# ~~~~~~~~ API URLS ~~~~~~~~~~~~
urlConfig = 'https://www.google.com'

# ~~~~~~~~ CONFIG VARIABLES ~~~~~~~~~
config = dict(
  running = True,
  transmitDelay = 300, # server send delay (in seconds)
  targetTemp = 70, # current target temperature (degrees farenheight)
  nextScheduledTime = 0, # time since epoch for next scheduled action (in seconds)
  nextScheduledTemp = 68 # scheduled temp (deg F)
)

def initializeApp():
  # Read from default config file and initialize config dictionary

def updateConfig():
  global config
  initURL = urlConfig
  res = requests.get(url = initURL)
  data = res.json()
  config = res['config']

def furnaceControl(turnFurnaceOn = furnaceOn):
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

def convertTemp(serializedTemp):
  # Convert temperature data from ADC value to deg Farenheight

def readConfig():
  # readConfig from static file

def writeConfig():
  # write config to static file

def scheduler(curTime):
  if (curTime >= nextScheduledTime):
    global config
    config['targetTemp'] = config['nextScheduledTemp']
    readSchedule(config['nextScheduledTime'])

def readSchedule(curTime):
  # Read schedule file and return nextScheduledTemp and nextScheduledTime

def ioTestToggle():
  furnaceControl(not furnaceOn)

def ioTestToggle():
  global config
  config['running'] = False

# Initialize listener on ioTestPin
GPIO.add_event_detect(ioTestPin, GPIO.RISING, callback=ioTestToggle(), bouncetime=200)
GPIO.add_event_detect(runTestPin, GPIO.RISING, callback=ioRunToggle(), bouncetime=20)

# Run scheduling process
while config['running']:
  global previousTime, config
  
  temp = readTemp()
  curTime = time.time()
  cycleTime = curTime - previousTime
  
  # Run scheduler
  scheduler(cycleTime)
  
  # Send stored temperature data
  if (cycleTime > transmitDelay):
    previousTime = time.time()
    sendTemp()
  
  sleep(.5)
