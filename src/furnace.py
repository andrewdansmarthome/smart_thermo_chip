import RPi.GPIO as GPIO
import time, threading, requests, json, sys
from env.env import ENV_API_URL, ENV_LOCATION_ID
from api_urls import apiFurnace

class Furnace:
  def __init__(self, furnacePin):
    self.furnacePin = furnacePin
    self.furnaceOn = False

  def furnaceToggle(self):
    if (not self.furnaceOn):
      GPIO.output(self.furnacePin, GPIO.HIGH)
      self.furnaceOn = True
    else:
      GPIO.output(self.furnacePin, GPIO.LOW)
      self.furnaceOn = False

  def ioTestToggle(self):
    self.furnaceToggle()
  
  def furnaceForceOff(self):
    GPIO.output(self.furnacePin, GPIO.LOW)
    self.furnaceOn = False
