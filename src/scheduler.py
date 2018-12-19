import time, threading, requests, json
from env.env import ENV_API_URL

# ~~~~~~~~ INIT VARIABLES ~~~~~~~~~
furnaceOn = False
previousTime = time.time()
running = True

# ~~~~~~~~ API URLS ~~~~~~~~~~~~
urlSchedule = ENV_API_URL + '/thermostat/scheduler'

# ~~~~~~~~ CONFIG VARIABLES ~~~~~~~~~
initSchedule = dict(
  chipId = 1,
  nextScheduledTime = time.time() + 300, # time since epoch for next scheduled action (in seconds)
  nextScheduledTemp = 68 # scheduled temp (deg F)
)

class Scheduler:
  def __init__(self, schedule):
    self.chipId = schedule['chipId']
    self.nextScheduledTemp = schedule['nextScheduledTemp']
    self.nextScheduledTime = schedule['nextScheduledTime']
  
  def scheduler(self, curTime):
    if (curTime >= self.nextScheduledTime):
      self.targetTemp = self.nextScheduledTemp
      self.getSchedule(self.nextScheduledTime)
  
  def getSchedule(self, curTime):
    # Read schedule file and return nextScheduledTemp and nextScheduledTime
    print('readSchedule fired!')
