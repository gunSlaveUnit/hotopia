from common.src.core.settings import *

CLIENT_ROOT = BASE_PATH / 'client'
RESOURCES_PATH = CLIENT_ROOT / 'resources'

SERVER_URL = f"http://{CONFIG['HOST']}:{CONFIG['PORT']}"
MEDIA_URL = f'{SERVER_URL}{MEDIA_PREFIX}'
API_V1_URL = f'{SERVER_URL}{API_VERSION_1_PREFIX}'
AUTH_URL = f'{API_V1_URL}{AUTH_ROUTER_PREFIX}'
SIGN_UP_URL = f'{AUTH_URL}{SIGN_UP_URL}'
SIGN_IN_URL = f'{AUTH_URL}{SIGN_IN_URL}'
SIGN_OUT_URL = f'{AUTH_URL}{SIGN_OUT_URL}'
ME_URL = f'{AUTH_URL}{ME_URL}'
HOBBIES_URL = f'{API_V1_URL}{HOBBIES_ROUTER_PREFIX}'
MODULES_URL = f'{API_V1_URL}{MODULES_ROUTER_PREFIX}'
UNITS_URL = f'{API_V1_URL}{UNITS_ROUTER_PREFIX}'
WALKTHROUGHES_URL = f'{API_V1_URL}{WALKTHROUGHES_ROUTER_PREFIX}'