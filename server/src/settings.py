from pathlib import Path

DEBUG = True

BASE_PATH = Path(__file__).resolve().parent.parent.parent
MEDIA_PATH = BASE_PATH / 'media'

API_PREFIX = '/api'
MEDIA_PREFIX = '/media'
AUTH_ROUTER_PREFIX = '/auth'
UNITS_ROUTER_PREFIX = '/units'
MODULES_ROUTER_PREFIX = '/modules'
HOBBIES_ROUTER_PREFIX = '/hobbies'
API_VERSION_1_PREFIX = API_PREFIX + '/v1'
WALKTHROUGHES_ROUTER_PREFIX = '/walkthroughes'

SIGN_UP_URL = '/sign-up'
SIGN_IN_URL = '/sign-in'

SESSION_TTL = 3 * 24 * 60 * 60
