import os
from decouple import config, RepositoryEnv


# Get the path to the .env file based on the current environment
def get_env_path():
    env = config('ENVIRONMENT', default='test')
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources', f'{env}.env')


# Load the environment variables from the specified .env file
env_path = get_env_path()
if os.path.exists(env_path):
    print(f"ENV File found at {env_path}")
    env_config = RepositoryEnv(env_path)
else:
    print(f"No ENV File found at {env_path}")

DEBUG_SETTING = True if config('ENVIRONMENT', default='development') == 'development' else False
DJANGO_SECRET_KEY = env_config.data.get('DJANGO_SECRET_KEY', "EMPTY")
OPENAI_API_KEY = env_config.data.get('OPENAI_API_KEY', "EMPTY")
GOOGLE_CLIENT_ID = env_config.data.get('GOOGLE_CLIENT_ID', "EMPTY")
GOOGLE_SECRET_KEY = env_config.data.get('GOOGLE_SECRET_KEY', "EMPTY")
print("done config")
