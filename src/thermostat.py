import RPi.GPIO as GPIO
import time, threading, requests, json, sys
from env_setup import ENV_API_URL, ENV_LOCATION_ID
from src.pin_setup import PinSetup
from src.config import Config, initConfig
from src.scheduler import Scheduler, initSchedule
from src.temperature import Temperature, initTemp
from src.furnace import Furnace

class Thermostat:
  def __init__(self, furnace, pins):
    GPIO.setmode(GPIO.BCM)

    # ~~~~~~~~ INIT THERMOSTAT DEPENDENCIES ~~~~~~~~
    self.pins = pins
    self.config = Config(initConfig)
    self.furnace = furnace
    self.scheduler = Scheduler(initSchedule, self.config.chipId)
    self.temperature = Temperature(initTemp, self.pins)

    self.running = True
    self.prevTime = int(time.time())
    GPIO.add_event_detect(self.pins.runTestPin, GPIO.RISING, callback=self.ioRunToggle, bouncetime=500)

  def ioRunToggle(self):
    self.running = not self.running

  def run(self):
    # Run scheduling process
    test_io = False
    if test_io == True:
        test_io = False
    try:
      while self.running:
        curTime = int(time.time())
        cycleTime = curTime - self.prevTime

        # Read Temperature and store it locally
        curTemp = self.temperature.readAndStoreTemp(curTime, self.scheduler.targetTemp, self.config.chipId)
        print(curTemp)

        # Run scheduler
        targetTemp = self.scheduler.checkSchedule(curTime)

        # Control furnace
        if (not self.furnace.ioOverride):
          if (curTemp < targetTemp - self.config.tempOffset):
            self.furnace.turnOn()
          if (curTemp > targetTemp + self.config.tempOffset):
            self.furnace.turnOff()

        # Send stored temperature data
        if (cycleTime > self.config.transmitDelay):
          self.prevTime = curTime
          self.temperature.sendTemp()

        time.sleep(1)

    except KeyboardInterrupt:
      self.furnace.turnOff()
      sys.exit(0)
      
    finally:
      self.furnace.turnOff()
      print("Runtime Error: ", sys.exc_info()) 
      sys.exit(0)
    sys.exit(0)
