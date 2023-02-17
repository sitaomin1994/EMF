import os
from dynaconf import Dynaconf

settings = Dynaconf(
    envvar_prefix="DYNACONF",
    settings_files=['settings.json', '.secrets.json'],
)

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))