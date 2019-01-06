import time, requests, json
from env_setup import ENV_API_URL
from api_urls import apiScheduler

# ~~~~~~~~ TEST CONFIG VARIABLES ~~~~~~~~~
initSchedule = dict(
  nextScheduledTime = int(time.time()) + 300, # time since epoch for next scheduled action (in seconds)
  nextScheduledTemp = 68 # scheduled temp (deg F)
)

class Scheduler:
  def __init__(self, schedule, chipId):
    self.targetTemp = schedule['nextScheduledTemp']
    self.nextScheduledTemp = schedule['nextScheduledTemp']
    self.nextScheduledTime = schedule['nextScheduledTime']
    self.chipId = chipId
  
  def checkSchedule(self, curTime):
    if (curTime >= self.nextScheduledTime):
      self.targetTemp = self.nextScheduledTemp
      self.getSchedule(self.nextScheduledTime)
    return self.targetTemp
  
  def getSchedule(self, curTime):
    # Read schedule file and return nextScheduledTemp and nextScheduledTime
    print('readSchedule fired!')
    payload = {
      'nextScheduledTemp': self.nextScheduledTemp,
      'nextScheduledTime': self.nextScheduledTime
    }
    res = requests.get(url = apiScheduler, params = payload)
    self.nextScheduledTemp = res['nextScheduledTemp']
    self.nextScheduledTime = res['nextScheduledTime']

  def readSchedule(self, curTime):
    # Read schedule file and return nextScheduledTemp and nextScheduledTime
    print('readSchedule fired!')
