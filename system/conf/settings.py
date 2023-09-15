import os
from datetime import timedelta
from enum import Enum


""" 启动app服务使用 """
# 启动app实例的name
DEFAULT_SERVICE_NAME = 'system'
# API log name
API_BASE_NAME = "api"
# Set default host
API_DEFAULT_HOST = "0.0.0.0"
# Set default port
API_DEFAULT_PORT = 8082
# Ser default url path
API_DEFAULT_URL = "/"
# Root directory for API
ROOT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))

""" 解决flask跨域的配置信息 """
# Set a time difference between the client and server
CORS_TIME_MINS = 30
# Set CORS Header
CORS_HEADERS = ",".join([
    "Accept",
    "Accept-Language",
    "Content-Language",
    "Remote-Mac-Address",
    "Remote-Ip",
    "Content-Type",
    "Authorization",
    "Content-MD5",
    "Range",
    "x-dn-signature-method",
    "x-dn-api-version",
    "x-dn-download-size",
    "x-dn-body-raw-size",
    "x-dn-compress-type",
    "x-dn-date",
    "x-sgi-security-token"
])
CORS_RESOURCES = "*"
CORS_MAX_AGE = timedelta(minutes=CORS_TIME_MINS)


class APIConfig(object):
    """Initialize Flask instance."""
    # Open testing mode
    TESTING = False
    # Open debug mode
    DEBUG = False
    # Set root directory
    ROOT_DIR = ROOT_DIRECTORY
    # Set default host and port
    HOST = API_DEFAULT_HOST
    PORT = API_DEFAULT_PORT
    BASE_PATH = API_DEFAULT_URL


base_path = os.path.abspath(".")


class SpiderDataFileConfig(Enum):
    ResourceDirectoryPath = os.path.join(base_path, 'resource')
    MatchDataFilePath = '../resource/match_datas.json'
    IndexDataFilePath = os.path.join(base_path, 'resource', 'odds_datas_2023-08-25.json')

