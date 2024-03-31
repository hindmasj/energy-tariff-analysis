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
import requests
import sys


class Configuration:
    DFLT_CONF_FILE = 'eta.conf'
    DFLT_ES_TOKEN_FILE = 'es_token'
    DFLT_ES_URL = "https://localhost:9200/"
    DFLT_ES_CRT = "http_ca.crt"

    SECT_ES = 'elasticsearch'
    OPT_ES_TOKEN = 'token_file'
    OPT_ES_URL = 'es_url'
    OPT_ES_CRT = 'es_crt'

    def __init__(self,argv):
        self.argv=argv
        self.args=self.parse_command_line(argv)
        self.config=self.load_config_file(self.args.config)
        self.verbose=self.args.verbose

    @classmethod
    def parse_command_line(cls,argv):
        parser = argparse.ArgumentParser(
            prog="Energy Tariff Analysis",
            description="Analyse energy tariffs against consumption and generation records",
            epilog="Load records into Elasticsearch"
        )
        parser.add_argument('-c', '--config', default=cls.DFLT_CONF_FILE)
        parser.add_argument('-v', '--verbose', action='store_true')
        return parser.parse_args()

    @classmethod
    def load_config_file(cls,config_file_name):
        config=configparser.ConfigParser()
        config['DEFAULT']={cls.OPT_ES_TOKEN:cls.DFLT_ES_TOKEN_FILE,
                           cls.OPT_ES_URL:cls.DFLT_ES_URL,
                           cls.OPT_ES_CRT:cls.DFLT_ES_CRT}
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

    def get_es_url(self):
        return self.config.get(self.SECT_ES,self.OPT_ES_URL)

    def get_es_crt_filename(self):
        return self.config.get(self.SECT_ES, self.OPT_ES_CRT)


class ElasticsearchClient:

    def __init__(self,config):
        self.config=config
        self.es_token=self.load_es_token(config.get_es_token_filename())
        self.session=requests.Session()
        self.session.headers.update({"Authorization": "ApiKey %s"%(self.es_token)})
        self.session.verify=config.get_es_crt_filename()
        self.url=config.get_es_url()

    @staticmethod
    def load_es_token(token_file_name):
        try:
            with open(token_file_name,'r') as token_file:
                token=token_file.read().replace('\n','')
        except OSError as e:
            print("Unable to load token file: %s"%(e))
            return None
        return token

    def check_connection(self):
        if not self.es_token:
            return False
        response=self.session.get(self.url)
        if not response.ok:
            print("Failed: %s, %s: %s"%(response.status_code, response.reason, response.text))
            return False
        if self.config.verbose:
            print(response.text)
        else:
            print("Connected")
        return True

if __name__ == '__main__':
    print('Welcome to the Energy Tariff Analysis script')
    config=Configuration(sys.argv)
    es_client=ElasticsearchClient(config)
    if not es_client.check_connection():
        print("Connection issues: see messages")
