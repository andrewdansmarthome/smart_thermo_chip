from env.secrets import URL_DEV_API, URL_PROD_API, LOCATION_ID
import main

def currentEnvURL(currentEnv):
  if (currentEnv == 'DEV'):
    return URL_DEV_API
  return URL_PROD_API

ENV_API_URL = currentEnvURL(main.envMode)
ENV_LOCATION_ID = LOCATION_ID
