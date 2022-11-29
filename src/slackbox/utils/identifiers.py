"""
created by: Thibault DEFEYTER
created at: 2022/11/29
license: MIT

slackbox unique identifiers management
"""

from math import ceil
from math import log
from os import urandom

from slackbox import config


def generate_identifier() -> str:
    """generate a random identifier"""
    alphabet_len = len(config.IDENTIFIER_ALPHABET)

    mask = 1
    if alphabet_len > 1:
        mask = (2 << int(log(alphabet_len - 1) / log(2))) - 1
    step = int(ceil(1.6 * mask * config.IDENTIFIER_SIZE / alphabet_len))

    identifier = ""
    while True:
        random_bytes = bytearray(urandom((step)))

        for i in range(step):
            if len(identifier) == config.IDENTIFIER_SIZE:
                return identifier

            random_byte = random_bytes[i] & mask
            if random_byte >= alphabet_len:
                continue
            identifier += config.IDENTIFIER_ALPHABET[random_byte]
