import RPi.GPIO as GPIO
import time, threading, requests
from env.env import ENV_API_URL

# ~~~~~~~~ DEFAULT CONFIG ~~~~~~~~~
initConfig = dict(
  chipId = 1,
  transmitDelay = 300, # server send delay (in seconds)
  processDelay = 300, # in seconds
)

# ~~~~~~~~ API URLS ~~~~~~~~~~~~
urlConfig = ENV_API_URL + '/thermostat/config'

class Config:
  def __init__(self, setup):
    self.chipId = setup['chipId']
    self.transmitDelay = setup['transmitDelay']
    self.processDelay = setup['processDelay']
  
  def updateConfig(self):
    res = requests.get(url = urlConfig)
    data = res.json()
    for item in data.keys():
      setattr(self, item, data[item])

  def readConfig(self):
    # readConfig from static file
    print('readConfig fired!')

  def writeConfig(self):
    # write config to static file
    print('writeConfig fired!')
    payload = self
    res = requests.post(url = urlConfig, json = payload)
    print('res: ', res)
    return res
