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


class Configuration:
    DFLT_CONF_FILE = 'eta.conf'
    DFLT_ES_TOKEN_FILE = 'es_token'

    SECT_ES = 'elasticsearch'
    OPT_ES_TOKEN = 'token_file'

    def __init__(self,argv):
        self.argv=argv
        self.args=self.parse_command_line(argv)
        self.config=self.load_config_file(self.args.config)

    @classmethod
    def parse_command_line(cls,argv):
        parser = argparse.ArgumentParser(
            prog="Energy Tariff Analysis",
            description="Analyse energy tariffs against consumption and generation records",
            epilog="Load records into Elasticsearch"
        )
        parser.add_argument('-c', '--config', default=cls.DFLT_CONF_FILE)
        return parser.parse_args()

    @classmethod
    def load_config_file(cls,config_file_name):
        config=configparser.ConfigParser()
        config['DEFAULT']={cls.OPT_ES_TOKEN:cls.DFLT_ES_TOKEN_FILE}
        config[cls.SECT_ES] = {}
        try:
            config.read(config_file_name)
        except FileNotFoundError:
            print("Config file not found, using defaults")
        except configparser.ParsingError as e:
            print("Config file not parsed: %s"%(e))
            sys.exit(1)
        return config

    def get_es_token_filename(self):
        return self.config.get(self.SECT_ES,self.OPT_ES_TOKEN)

class ElasticsearchClient:

    def __init__(self,config):
        self.config=config
        self.es_token=self.load_es_token(config.get_es_token_filename())

    @staticmethod
    def load_es_token(token_file_name):
        try:
            with open(token_file_name,'r') as token_file:
                return token_file.read
        except OSError as e:
            print("Unable to load token file: %s"%(e))
            return None

    def check_connection(self):
        if not self.es_token:
            return False
        return True

if __name__ == '__main__':
    print('Welcome to the Energy Tariff Analysis script')
    config=Configuration(sys.argv)
    es_client=ElasticsearchClient(config)
    es_client.check_connection()
