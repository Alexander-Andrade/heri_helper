import environ
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
env = environ.Env(DEBUG=(bool, False))
env_file = os.path.join(BASE_DIR, ".env")
environ.Env.read_env(env_file)


CHROME_DRIVER_PATH = env.str('CHROME_DRIVER_PATH')
LINKEDIN_EMAIL = env.str('LINKEDIN_EMAIL')
LINKEDIN_PASSWORD = env.str('LINKEDIN_PASSWORD')
ATS_EMAIL = env.str('ATS_EMAIL')
ATS_PASSWORD = env.str('ATS_PASSWORD')
MAX_PAGE = env.int('MAX_PAGE')
