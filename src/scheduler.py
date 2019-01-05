import time, requests, json
from env.env import ENV_API_URL
from api_urls import apiScheduler

# ~~~~~~~~ TEST CONFIG VARIABLES ~~~~~~~~~
initSchedule = dict(
  nextScheduledTime = time.time() + 300, # time since epoch for next scheduled action (in seconds)
  nextScheduledTemp = 68 # scheduled temp (deg F)
)

class Scheduler:
  def __init__(self, schedule):
    self.targetTemp = schedule['nextScheduledTemp']
    self.nextScheduledTemp = schedule['nextScheduledTemp']
    self.nextScheduledTime = schedule['nextScheduledTime']
  
  def scheduler(self, curTime):
    if (curTime >= self.nextScheduledTime):
      self.targetTemp = self.nextScheduledTemp
      self.getSchedule(self.nextScheduledTime)
  
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
