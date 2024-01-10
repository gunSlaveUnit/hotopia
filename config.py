from pathlib import Path

from dotenv import dotenv_values

BASE_PATH = Path(__file__).resolve().parent


CONFIG = dotenv_values(BASE_PATH / '.env')

# Server use prefixes and URLs as is.
# Client construct URLs from them.
MEDIA_PREFIX = '/media'
API_PREFIX = '/api'
API_VERSION_1_PREFIX = API_PREFIX + '/v1'
AUTH_ROUTER_PREFIX = '/auth'
SIGN_UP_URL = '/sign-up'
SIGN_IN_URL = '/sign-in'
SIGN_OUT_URL = '/sign-out'
ME_URL = '/me'
HOBBIES_ROUTER_PREFIX = '/hobbies'
MODULES_ROUTER_PREFIX = '/modules'
UNITS_ROUTER_PREFIX = '/units'
WALKTHROUGHES_ROUTER_PREFIX = '/walkthroughes'
