#!/usr/bin/env python3
# Energy Tariff Analysis
# Calculate tariff costs based on usage and export data stored in Elasticsearch

# This script is adapted from the PyCharm sample main.py.
# Press Shift+F10 to execute it.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
# Press the green button in the gutter to run the script.
# See PyCharm help at https://www.jetbrains.com/help/pycharm/

import argparse
import configparser
import sys

DFLT_CONF_FILE='eta.conf'
DFLT_ES_TOKEN_FILE='es_token'

SECT_ES='elasticsearch'
OPT_ES_TOKEN='token_file'


def parse_command_line(argv):
    parser = argparse.ArgumentParser(
        prog="Energy Tariff Analysis",
        description="Analyse energy tariffs against consumption and generation records",
        epilog="Load records into Elasticsearch"
    )
    parser.add_argument('-c', '--config', default=DFLT_CONF_FILE)
    return parser.parse_args()

def load_config_file(config_file_name):
    config=configparser.ConfigParser()
    config['DEFAULT']={OPT_ES_TOKEN:DFLT_ES_TOKEN_FILE}
    config[SECT_ES] = {}
    try:
        config.read(config_file_name)
    except FileNotFoundError:
        print("Config file not found, using defaults")
    except configparser.ParsingError as e:
        print("Config file not parsed: %s"%(e))
        sys.exit(1)
    return config

def load_es_token(token_file_name):
    try:
        with open(token_file_name,'r') as token_file:
            return token_file.read
    except OSError as e:
        print("Unable to load token file: %s"%(e))
        sys.exit(2)

if __name__ == '__main__':
    print('Welcome to the Energy Tariff Analysis script')
    args=parse_command_line(sys.argv)
    config=load_config_file(args.config)
    es_token=load_es_token(config.get(SECT_ES,OPT_ES_TOKEN))
