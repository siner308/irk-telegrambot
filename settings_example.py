import os

# # # # # # # # # # # #
# Siner Configuration #
# # # # # # # # # # # #
try:
    TEST = os.environ['TEST']
except:
    TEST = None

if TEST:
    SERVER_URL = 'http://127.0.0.1:5784'
    TOKEN = 'XXXXXXXXXX'
else:
    SERVER_URL = 'XXXXXXXXXXXXXXXX'
    TOKEN = 'XXXXXXXXXXXXXX'

LOG_DIR = '/app/log/bot'
STATIC_ROOT = '/app/html'
CHROMEDRIVER_PATH = os.path.dirname(os.path.realpath(__file__)) + '/chromedriver'

# Ingress
GOOGLE_EMAIL = 'XXXXXXXXXXXXXXXX'
GOOGLE_PASSWORD = 'XXXXXXXXXXXXX'
INGRESS_AGENT_NAME = 'XXXXXXXXXXXXXXXXXX'
GOOGLE_MAP_KEY = 'XXXXXXXXXXXXX'
MAX_LOAD_TIME = 300

# Giphy
GIPHY_KEY = 'XXXXXXXXXX'
