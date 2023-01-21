"""
created by: Thibault DEFEYTER
created at: 2022/11/29
licene: MIT

slackbox configuration
"""

from os import getenv


def get_string(key: str, default: str) -> str:
    """return string value from env variables"""
    return getenv(key, default)


# general config
SERVICE = get_string("SERVICE", "slackbox")
VERSION = get_string("VERSION", "dev")

# identifier generation configuration
IDENTIFIER_ALPHABET = "abcdefghijklmnopqrstuvxyz"
IDENTIFIER_SIZE = 8

# slack configuration
SLACK_BOT_TOKEN = get_string("SLACK_BOT_TOKEN", "token")
SLACK_SIGNING_SECRET = get_string("SLACK_SIGNING_SECRET", "secret")
