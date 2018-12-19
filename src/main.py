# Main runtime of the program. To run, type: python3 main.py
import thermostat

def initializeApp():
  # Read from default config file and initialize config dictionary
  print('all functions must have actual code in them')
  global config
  res = requests.get(urlConfig + config['id'])
  data = res.json()
  print('data', data)
  config = data['config']

# app runtime
initializeApp()
while running:
  