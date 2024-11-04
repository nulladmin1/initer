import argparse
from os import path, makedirs
from requests import get
from subprocess import call
from urllib.parse import urlparse
import yaml


CONF_DIR_LOCATION: str = f"{path.expanduser('~/.config/initer')}"
CONF_LOCATION: str = f"{CONF_DIR_LOCATION + '/initer.yaml'}"

parser = argparse.ArgumentParser()

parser.add_argument('mode', help='Picks the code mode from config file.')

args = parser.parse_args()


def get_config() -> yaml.YAMLObject:
    if path.isdir(CONF_DIR_LOCATION):
        pass
    else:
        makedirs(CONF_DIR_LOCATION)
    with open(CONF_LOCATION, 'r') as f:
        data = yaml.safe_load(f)
        f.close()
        return data


def config_exec(configuration: yaml.YAMLObject, code_mode: str):
    for command in configuration['Modes'][code_mode]['exec']:
        c = command.split()
        call(c)


def config_download(configuration: yaml.YAMLObject, code_mode: str):
    for down in configuration['Modes'][code_mode]['download']:
        response = get(down, stream=True)
        url = urlparse(down)
        filename = url.path.split('/')[-1]
        with open(filename, "wb") as f:
            for chunk in response.iter_content(chunk_size=4096):
                f.write(chunk)
        f.close()


config = get_config()

mode = args.mode.lower().capitalize()

config_download(config, mode)
config_exec(config, mode)
