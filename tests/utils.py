"""
created by: Thibault DEFEYTER
created at: 2022/11/29
license: MIT

slackbox test utilities
"""

import re
from typing import Optional


class AnyInstanceOf:
    """Class being to any instance of 'klass'"""

    def __init__(self, klass):
        self.klass = klass

    def __eq__(self, other):
        if not isinstance(other, self.klass):
            return False
        return True

    def __repr__(self):
        return f"AnyInstanceOf({self.klass.__name__})"


class AnyStringMatching:
    """Class being equal to any string matching a given regexp"""

    regexp: re.Pattern

    def __init__(self, regexp: Optional[str] = None):
        if regexp:
            self.regexp = re.compile(regexp)

    def __eq__(self, other):
        if not isinstance(other, str):
            return False
        return bool(re.match(self.regexp, other))

    def __repr__(self):
        return f"{self.__class__.__name__}()"


class AnyDatetimeString(AnyStringMatching):
    """Class being equal to any iso datetime string"""

    regexp = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}", re.I)


class AnyPublicID(AnyStringMatching):
    """Class being equal to any public id string"""

    regexp = re.compile(r"[a-z]{8}")
