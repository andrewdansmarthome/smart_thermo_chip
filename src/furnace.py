import RPi.GPIO as GPIO
import time, threading, requests, json, sys
from env.env import ENV_API_URL, ENV_LOCATION_ID

class Furnace:
  def __init__(self, pins):
    self.furnacePin = pins.furnacePin
    self.furnaceOn = False
    GPIO.add_event_detect(pins.ioTestPin, GPIO.FALLING, callback=self.ioTestToggle, bouncetime=200)

  def turnOn(self):
    GPIO.output(self.furnacePin, GPIO.HIGH)
    self.furnaceOn = True
  
  def turnOff(self):
    GPIO.output(self.furnacePin, GPIO.LOW)
    self.furnaceOn = False

  def ioTestToggle(self):
    if (self.furnaceOn):
      GPIO.output(self.furnacePin, GPIO.LOW)
    else:
      GPIO.output(self.furnacePin, GPIO.HIGH)
    self.furnaceOn = not self.furnaceOn



  def furnaceForceOff(self):
    GPIO.output(self.furnacePin, GPIO.LOW)
    self.furnaceOn = False


