"""
created by: Thibault DEFEYTER
created at: 2022/11/29
license: MIT

slackbox string management
"""

import re
from enum import Enum
from typing import Callable


class Case(Enum):
    """possible string cases"""

    SNAKE = "snake"
    CAMEL = "camel"
    KEBAB = "kebab"
    PASCAL = "pascal"


class CaseValidator:
    """Expose method validating string's cases"""

    @classmethod
    def get_validator(cls, case: Case) -> Callable[[str], bool]:
        """get the validator for the given case"""
        validator_name = f"is_{case.value}"
        if not hasattr(cls, validator_name):
            raise NotImplementedError(f"CaseValidator.{validator_name}")
        return getattr(cls, validator_name)

    @staticmethod
    def is_camel(string: str) -> bool:
        """make sure the string is camel case"""
        return bool(re.match("^[a-z]+([A-Z]+[a-z]+)*$", string))

    @staticmethod
    def is_snake(string: str) -> bool:
        """make sure the string is snake case"""
        return bool(re.match("^[a-z]+(_[a-z]+)*$", string))

    @staticmethod
    def is_kebab(string: str) -> bool:
        """make sure the string is kebab case"""
        return bool(re.match("^[a-z]+(-[a-z]+)*$", string))

    @staticmethod
    def is_pascal(string: str) -> bool:
        """make sure the string is pascal case"""
        return bool(re.match("^([A-Z]+[a-z]+)+$", string))


class CaseEnforcer:
    """Expose method enforcing a string's case"""

    @classmethod
    def get_enforcer(cls, case: Case) -> Callable[[str], str]:
        """get the enforcer for the given case"""
        enforcer_name = f"to_{case.value}"
        if not hasattr(cls, enforcer_name):
            raise NotImplementedError(f"CaseValidator.{enforcer_name}")
        return getattr(cls, enforcer_name)

    @classmethod
    def get_components(cls, string: str) -> list[str]:
        """extract components from any case string"""
        component_string = re.sub(r"(_|-)+", " ", string)
        component_string = re.sub(r"([A-Z])", r" \g<1>", component_string)
        component_string = component_string.lower()
        component_string = component_string.replace("'", " ")
        component_string = component_string.replace('"', " ")
        component_string = component_string.strip()
        return component_string.split(" ")

    @classmethod
    def to_camel(cls, string: str) -> str:
        """force the string to camel case"""
        components = cls.get_components(string)
        return components[0] + "".join(x.title() for x in components[1:])

    @classmethod
    def to_snake(cls, string: str) -> str:
        """force the string to snake case"""
        return "_".join(cls.get_components(string))

    @classmethod
    def to_kebab(cls, string: str) -> str:
        """force the string to kebab case"""
        return "-".join(cls.get_components(string))

    @classmethod
    def to_pascal(cls, string: str) -> str:
        """force the string to pascal case"""
        components = cls.get_components(string)
        return "".join(x.title() for x in components)


class CaseConverter:
    """Expose methods transforming string from one case to others"""

    @classmethod
    def get_converter(cls, from_case: Case, to_case: Case) -> Callable[[str], str]:
        """get the converter from one case to another"""
        converter_name = f"convert_{from_case.value}_to_{to_case.value}"
        if not hasattr(cls, converter_name):
            raise NotImplementedError(f"CaseConverter.{converter_name}")
        return getattr(cls, converter_name)

    @staticmethod
    def convert_snake_to_camel(string: str) -> str:
        """convert a snake cased string to camel case"""
        components = string.split("_")
        return components[0] + "".join(x.title() for x in components[1:])

    @staticmethod
    def convert_snake_to_kebab(string: str) -> str:
        """convert a snake cased string to kebab case"""
        return string.replace("_", "-")

    @staticmethod
    def convert_snake_to_pascal(string: str) -> str:
        """convert a snake cased string to pascal case"""
        return "".join(x.title() for x in string.split("_"))

    @staticmethod
    def convert_camel_to_snake(string: str) -> str:
        """convert a camel cased string to snake case"""
        return re.sub("([A-Z])", r"_\1", string).lower()

    @staticmethod
    def convert_camel_to_kebab(string: str) -> str:
        """convert a camel cased string to kebab case"""
        return re.sub("([A-Z])", r"-\1", string).lower()

    @staticmethod
    def convert_camel_to_pascal(string: str) -> str:
        """convert a camel cased string to pascal case"""
        return f"{string[0].upper()}{string[1:]}"

    @staticmethod
    def convert_kebab_to_snake(string: str) -> str:
        """convert a kebab cased string to snake case"""
        return string.replace("-", "_")

    @staticmethod
    def convert_kebab_to_camel(string: str) -> str:
        """convert a kebab cased string to camel case"""
        components = string.split("-")
        return components[0] + "".join(x.title() for x in components[1:])

    @staticmethod
    def convert_kebab_to_pascal(string: str) -> str:
        """convert a kebab cased string to pascal case"""
        return "".join(x.title() for x in string.split("-"))

    @staticmethod
    def convert_pascal_to_snake(string: str) -> str:
        """convert a pascal cased string to snake case"""
        return re.sub("([A-Z])", r"_\1", string).lower().strip("_")

    @staticmethod
    def convert_pascal_to_camel(string: str) -> str:
        """convert a pascal cased string to camel case"""
        return f"{string[0].lower()}{string[1:]}"

    @staticmethod
    def convert_pascal_to_kebab(string: str) -> str:
        """convert a pascal cased string to kebab case"""
        return re.sub("([A-Z])", r"-\1", string).lower().strip("-")


def convert_case(string: str, from_case: Case, to_case: Case) -> str:
    """convert a string from one case to another"""
    is_valid = CaseValidator.get_validator(from_case)
    if not is_valid(string):
        raise ValueError(f"{string} is not a {from_case.value} case string")
    convert = CaseConverter.get_converter(from_case, to_case)
    return convert(string)


def force_case(string: str, case: Case) -> str:
    """force the string to the given case"""
    enforce = CaseEnforcer.get_enforcer(case)
    return enforce(string)
