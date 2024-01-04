from pathlib import Path

DEBUG = True

RELOAD = True

SESSION_TTL = 3 * 24 * 60 * 60

BASE_PATH = Path(__file__).resolve().parent.parent.parent.parent
MEDIA_PATH = BASE_PATH / 'media'
