import RPi.GPIO as GPIO
import time, threading, requests, json, sys
from env_setup import ENV_API_URL, ENV_LOCATION_ID

class Furnace:
  def __init__(self, pins):
    self.furnacePin = pins.furnacePin
    self.furnaceOn = False
    self.ioOverride = False
    GPIO.add_event_detect(pins.ioTestPin, GPIO.FALLING, callback=self.ioTestToggle, bouncetime=500)

  def turnOn(self):
    print('Furnace turned ON')
    GPIO.output(self.furnacePin, GPIO.HIGH)
    self.furnaceOn = True
  
  def turnOff(self):
    print('Furnace turned OFF')
    GPIO.output(self.furnacePin, GPIO.LOW)
    self.furnaceOn = False

  def ioTestToggle(self, pin):
    if (self.furnaceOn):
      GPIO.output(self.furnacePin, GPIO.LOW)
    else:
      GPIO.output(self.furnacePin, GPIO.HIGH)
    self.furnaceOn = not self.furnaceOn
    self.ioOverride = not self.ioOverride
    print('Toggled furnace to: ', self.ioOverride)



  def furnaceForceOff(self):
    GPIO.output(self.furnacePin, GPIO.LOW)
    self.furnaceOn = False


