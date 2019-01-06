import RPi.GPIO as GPIO
import time, threading, requests, json, spidev, sys
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

from env_setup import ENV_API_URL, ENV_LOCATION_ID

GPIO.setmode(GPIO.BCM)
mcp = Adafruit_MCP3008.MCP3008(clk = 21, cs = 8, miso = 19, mosi = 20)
# ~~~~~~~~~ SPI SETUP ~~~~~~~
bus = 0
device = 0
spi = spidev.SpiDev()
spi.open(bus, device)
spi.max_speed_hz = 488000

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

def buildReadCommand(channel):
  startBit = 0x01
  singleEnded = 0x08
  return [startBit, singleEnded | (channel << 4), 0]

def processAdcValue(result):
  byte2 = (result[1] & 0x03)
  return (byte2 << 8) | result[2]

def readAdc(channel):
  msg = 0b11
  msg = ((msg << 1) + channel) << 5
  msg = [msg, 0b00000000]
  reply = spi.xfer2(msg)
  adc = 0
  for n in reply:
    adc = (adc << 8) + n
  adc = adc >> 1
  voltage = (5 * adc) / 1024
  print("msg: ", msg, 'reply: ', reply, "adc: ", adc, "voltage: ", voltage)
  return adc

# Initialize listener on ioTestPin
GPIO.add_event_detect(ioTestPin, GPIO.FALLING, callback=ioTestToggle, bouncetime=200)
GPIO.add_event_detect(runTestPin, GPIO.RISING, callback=ioRunToggle, bouncetime=200)

sendConfig()

# Run scheduling process
try: 
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
    sensorTemp = readAdc(0)
    print("temp: ", sensorTemp, str(sensorTemp))
    values = [0]*8
    for i in range(8):
      values[i] = mcp.read_adc(i)
    print(' | {0:>4}  | {1:>4}  | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4}  | {7:>4} |'.format(*values))
    time.sleep(5)
except KeyboardInterrupt: 
  spi.close()
  sys.exit(0)
