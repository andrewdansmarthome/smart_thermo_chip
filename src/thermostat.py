import RPi.GPIO as GPIO
import time, threading, requests, json, sys
from env.env import ENV_API_URL, ENV_LOCATION_ID
from config import Config, initConfig
from scheduler import Scheduler
from temperature import Temperature, initTemp
from pin_setup import PinSetup
from furnace import Furnace

# ~~~~~~~~ INIT THERMOSTAT DEPENDENCIES ~~~~~~~~
pins = PinSetup()
config = Config(initConfig)
furnace = Furnace(pins)
scheduler = Scheduler(config.chipId)
temperature = Temperature(initTemp, pins)


class Thermostat:
  def __init__(self):
    self.running = True
    self.prevTime = int(time.time())
    GPIO.add_event_detect(pins.runTestPin, GPIO.RISING, callback=self.ioRunToggle, bouncetime=200)

  def ioRunToggle(self):
    self.running = False

  def run(self):
    # Run scheduling process
    try:
      while self.running:
        curTime = int(time.time())
        cycleTime = curTime - self.prevTime

        #readTemperature
        curTemp = temperature.readTemp()

        # Run scheduler
        targetTemp = scheduler.checkSchedule(curTime)

        # Control furnace
        if (curTemp < targetTemp - config.tempOffset):
          furnace.turnOn()
        if (curTemp > targetTemp + config.tempOffset):
          furnace.turnOff()

        # Send stored temperature data
        if (cycleTime > config.processDelay):
          self.prevTime = curTime
          temperature.sendTemp()

        print('ioTestPin: ', GPIO.input(pins.ioTestPin), 'runTestPin: ', GPIO.input(pins.runTestPin), 'cycleTime: ', cycleTime)
        time.sleep(5)
    except KeyboardInterrupt:
      sys.exit(0)
