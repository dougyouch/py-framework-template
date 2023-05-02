import argparse
import os

def add_test_option(required=True):
    default = os.environ.get('TEST')
    required = (required and default == None)
    OPTION_PARSER.add_argument('-t', '--test', help='Test', default=default, required=required)

# create a default option parser for all scripts
OPTION_PARSER = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

# add the environment option
default = os.environ.get('APP_ENV')
required = default == None
OPTION_PARSER.add_argument('-e', '--environment', help='Environment', choices=['stage', 'staging', 'prod', 'production', 'dev', 'development', 'local'], default=default, required=required)
