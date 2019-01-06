import RPi.GPIO as GPIO
import requests
from env_setup import ENV_API_URL
from api_urls import apiConfig

# ~~~~~~~~ DEFAULT CONFIG ~~~~~~~~~
initConfig = dict(
  chipId = '1',
  transmitDelay = 30, # server send delay (in seconds)
  processDelay = 300, # in seconds
  tempOffset = 2
)

class Config:
  def __init__(self, setup):
    self.chipId = setup['chipId']
    self.transmitDelay = setup['transmitDelay']
    self.processDelay = setup['processDelay']
    self.configApi = apiConfig + setup['chipId']
    self.tempOffset = setup['tempOffset']
  
  def updateConfig(self):
    res = requests.get(url = self.configApi)
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
    res = requests.post(url = self.configApi, json = payload)
    print('res: ', res)
    return res
  
  def sendConfig(self, config):
    # updating config in db
    requests.post(self.configApi, json=config)
