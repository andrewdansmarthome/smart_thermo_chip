import RPi.GPIO as GPIO
import time, threading, requests, json, sys
from env_setup import ENV_API_URL, ENV_LOCATION_ID
from src.pin_setup import PinSetup
from src.config import Config, initConfig
from src.scheduler import Scheduler, initSchedule
from src.temperature import Temperature, initTemp
from src.furnace import Furnace

GPIO.setmode(GPIO.BCM)

# ~~~~~~~~ INIT THERMOSTAT DEPENDENCIES ~~~~~~~~
pins = PinSetup()
config = Config(initConfig)
furnace = Furnace(pins)
scheduler = Scheduler(initSchedule, config.chipId)
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

        # Read Temperature and store it locally
        curTemp = temperature.readAndStoreTemp(curTime, scheduler.targetTemp, config.chipId)

        # Run scheduler
        targetTemp = scheduler.checkSchedule(curTime)

        # Control furnace
        if (curTemp < targetTemp - config.tempOffset):
          furnace.turnOn()
        if (curTemp > targetTemp + config.tempOffset):
          furnace.turnOff()

        # Send stored temperature data
        if (cycleTime > config.transmitDelay):
          self.prevTime = curTime
          temperature.sendTemp()

        time.sleep(1)
    except KeyboardInterrupt:
      sys.exit(0)
