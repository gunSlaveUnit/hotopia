from server.src.settings import HOST, PORT, AUTH_ROUTER_PREFIX, API_VERSION_1_PREFIX, SIGN_UP_URL, SIGN_IN_URL, \
    SIGN_OUT_URL, ME_URL, HOBBIES_ROUTER_PREFIX

SERVER_URL = f'http://{HOST}:{PORT}'
API_V1_URL = f'{SERVER_URL}{API_VERSION_1_PREFIX}'
AUTH_URL = f'{API_V1_URL}{AUTH_ROUTER_PREFIX}'
SIGN_UP_URL = f'{AUTH_URL}{SIGN_UP_URL}'
SIGN_IN_URL = f'{AUTH_URL}{SIGN_IN_URL}'
SIGN_OUT_URL = f'{AUTH_URL}{SIGN_OUT_URL}'
ME_URL = f'{AUTH_URL}{ME_URL}'
HOBBIES_URL = f'{API_V1_URL}{HOBBIES_ROUTER_PREFIX}'
