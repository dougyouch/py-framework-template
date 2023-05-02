import os
import sys
import logging
from script_options import OPTION_PARSER

def get_app_env():
    match SCRIPT_OPTIONS.environment:
      case 'prod':
        return 'production'
      case 'stage':
        return 'staging'
      case 'dev':
        return 'development'

    return SCRIPT_OPTIONS.environment

def get_app_prefix():
    match SCRIPT_OPTIONS.environment:
      case 'production':
        return 'prod'
      case 'staging':
        return 'stage'
      case 'development':
        return 'dev'

    return SCRIPT_OPTIONS.environment

def get_aws_profile():
    # TODO: map the environment to the correct AWS account
    # match APP_ENV:
    #   case 'production':
    #     return 'companyxprod'
    #   case 'staging':
    #     return 'companyxstage'

    return 'default'

# checks to see if the script is running locally
def is_running_locally():
    if os.environ.get('HOME') == None:
        return False

    aws_credentials_file_path = os.path.abspath(os.getenv('HOME') + '/.aws/credentials')
    return os.path.isfile(aws_credentials_file_path)

# loads secrets into the environment
def load_secrets(secret_name):
    import boto3
    import json

    secrets_manager = boto3.client('secretsmanager')
    response = secrets_manager.get_secret_value(SecretId=APP_PREFIX + '/' + secret_name)
    secrets = json.loads(response['SecretString'])

    for key in secrets:
        os.environ[key] = str(secrets[key])

def load_yaml(file_path):
    from yaml import load, Loader
    file = open(file_path, 'r')
    config = load(file.read(), Loader=Loader)
    file.close
    return config

def create_logger():
    logger = logging.getLogger('et-data-sync')
    formatter = logging.Formatter('%(asctime)s - ' + SCRIPT_NAME + '[%(process)d] - %(levelname)s: %(message)s')

    # Stream to STDOUT
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)

    logger.addHandler(ch)
    logger.setLevel(logging.INFO)

    return logger

BASE_DIR = os.path.abspath(__file__ + '/../..')
TMP_DIR = os.path.abspath(BASE_DIR + '/tmp')

SCRIPT_OPTIONS = OPTION_PARSER.parse_args()

APP_ENV=get_app_env() # ex: production
APP_PREFIX=get_app_prefix() # ex: prod

SCRIPT_NAME = os.path.basename(sys.argv[0])
LOG = create_logger()

# ensure the region is configured
if os.environ.get('AWS_DEFAULT_REGION') == None:
    os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'

if is_running_locally():
    # set the profile
    os.environ['AWS_PROFILE'] = get_aws_profile()

    # remove the AWS key/secret in favor of using the AWS profile
    if os.environ.get('AWS_ACCESS_KEY_ID') != None:
        del os.environ['AWS_ACCESS_KEY_ID']
    if os.environ.get('AWS_SECRET_ACCESS_KEY') != None:
      del os.environ['AWS_SECRET_ACCESS_KEY']
