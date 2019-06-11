import RPi.GPIO as GPIO
import time, threading, requests, json, sys
from env_setup import ENV_API_URL, ENV_LOCATION_ID

class AirCon:
  def __init__(self, pins):
    self.airConPin = pins.airConPin
    self.airConOn = False
    GPIO.add_event_detect(pins.ioTestPin, GPIO.FALLING, callback=self.ioTestToggle, bouncetime=200)

  def turnOn(self):
    GPIO.output(self.airConPin, GPIO.HIGH)
    self.airConOn = True
  
  def turnOff(self):
    GPIO.output(self.airConPin, GPIO.LOW)
    self.airConOn = False

  def ioTestToggle(self):
    if (self.airConOn):
      GPIO.output(self.airConPin, GPIO.LOW)
    else:
      GPIO.output(self.airConPin, GPIO.HIGH)
    self.airConOn = not self.airConOn



  def airConForceOff(self):
    GPIO.output(self.airConPin, GPIO.LOW)
    self.airConOn = False


