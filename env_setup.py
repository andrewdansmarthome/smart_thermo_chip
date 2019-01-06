import sys
from env.secrets import URL_DEV_API, URL_PROD_API, LOCATION_ID

# For dev mode, run with command: python3 main.py DEV

envMode = sys.argv[1]
print('current mode: ', envMode)

def currentEnvURL(currentEnv):
  if (currentEnv == 'DEV'):
    return URL_DEV_API
  return URL_PROD_API

ENV_API_URL = currentEnvURL(envMode)
ENV_LOCATION_ID = LOCATION_ID
