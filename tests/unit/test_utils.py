"""
created by: Thibault DEFEYTER
created at: 2022/11/29
license: MIT

unit testing slackbox utilities
"""

import re
from typing import Any

import pytest

from slackbox.utils.identifiers import generate_identifier
from slackbox.utils.strings import Case
from slackbox.utils.strings import CaseConverter
from slackbox.utils.strings import CaseEnforcer
from slackbox.utils.strings import CaseValidator
from slackbox.utils.strings import convert_case
from slackbox.utils.strings import force_case


def test_generate_identifier__format():
    """test identifier generation format"""
    public_id = generate_identifier()
    assert re.match("^[a-z]{8}$", public_id)


def test_generate_identifier__unicity():
    """test identifier generation unicity"""
    first_public_id = generate_identifier()
    second_public_id = generate_identifier()
    assert first_public_id != second_public_id


@pytest.mark.parametrize(
    "string, result",
    (
        ("snake_case", True),
        ("snake_case_case", True),
        ("snakecase", True),
        ("_snake_case", False),
        ("snake_case_", False),
        ("_snake_case_", False),
        ("snake__case", False),
        ("snake_cAse", False),
        ("snakecAse", False),
        ("snake case", False),
        ("snake -case", False),
    ),
)
def test_is_valid_snake(string: str, result: bool):
    """test snake case validation"""
    assert CaseValidator.is_snake(string) == result


@pytest.mark.parametrize(
    "string, result",
    (
        ("camelCase", True),
        ("camelCaseCase", True),
        ("camelCCase", True),
        ("camelCASECase", True),
        ("camelcase", True),
        ("Camelcase", False),
        ("camelcasE", False),
        ("CamelcasE", False),
        ("camel_case", False),
        ("camel_Case", False),
        ("camel-case", False),
        ("camel-Case", False),
        ("camel case", False),
        ("camel Case", False),
    ),
)
def test_is_valid_camel(string: str, result: bool):
    """test camel case validation"""
    assert CaseValidator.is_camel(string) == result


@pytest.mark.parametrize(
    "string, result",
    (
        ("kebab-case", True),
        ("kebab-case-case", True),
        ("kebabcase", True),
        ("-kebab-case", False),
        ("kebab-case-", False),
        ("-kebab-case-", False),
        ("kebab--case", False),
        ("kEbab-caSe", False),
        ("kEbabcaSe", False),
        ("kebab case", False),
        ("kebab -case", False),
    ),
)
def test_is_valid_kebab(string: str, result: bool):
    """test kebab case validation"""
    assert CaseValidator.is_kebab(string) == result


@pytest.mark.parametrize(
    "string, result",
    (
        ("PascalCase", True),
        ("PascalCaseCase", True),
        ("PascalCCase", True),
        ("PAscalCase", True),
        ("PascalCAse", True),
        ("pascalcase", False),
        ("PascalCasE", False),
        ("pascal case", False),
        ("Pascal Case", False),
    ),
)
def test_is_valid_pascal(string: str, result: bool):
    """test pascal case validation"""
    assert CaseValidator.is_pascal(string) == result


@pytest.mark.parametrize(
    "string, case, result",
    (
        ("snake_case", Case.SNAKE, True),
        ("snake_case", Case.CAMEL, False),
        ("snake_case", Case.KEBAB, False),
        ("snake_case", Case.PASCAL, False),
        ("camelCase", Case.SNAKE, False),
        ("camelCase", Case.CAMEL, True),
        ("camelCase", Case.KEBAB, False),
        ("camelCase", Case.PASCAL, False),
        ("kebab-case", Case.SNAKE, False),
        ("kebab-case", Case.CAMEL, False),
        ("kebab-case", Case.KEBAB, True),
        ("kebab-case", Case.PASCAL, False),
        ("PascalCase", Case.SNAKE, False),
        ("PascalCase", Case.CAMEL, False),
        ("PascalCase", Case.KEBAB, False),
        ("PascalCase", Case.PASCAL, True),
    ),
)
def test_validator(string: str, case: Case, result: bool):
    """test case validation"""
    is_valid = CaseValidator.get_validator(case)
    assert is_valid(string) == result


@pytest.mark.parametrize(
    "string, components",
    (
        ("normal case", ["normal", "case"]),
        ("snake_case", ["snake", "case"]),
        ("camelCase", ["camel", "case"]),
        ("kebab-case", ["kebab", "case"]),
        ("PascalCase", ["pascal", "case"]),
        ("Pascal-kebabCase", ["pascal", "kebab", "case"]),
        ("camel_snake case", ["camel", "snake", "case"]),
        ("I'm a teapot", ["i", "m", "a", "teapot"]),
        ("HTTPRequest", ["h", "t", "t", "p", "request"]),
    ),
)
def test_enforcer__get_components(string: str, components: list[str]):
    """test string components extraction, hidden heart of the case enforcing logic"""
    assert CaseEnforcer.get_components(string) == components


@pytest.mark.parametrize(
    "string, from_case, to_case, result",
    (
        ("snake_case", Case.SNAKE, Case.KEBAB, "snake-case"),
        ("snake_case", Case.SNAKE, Case.CAMEL, "snakeCase"),
        ("snake_case", Case.SNAKE, Case.PASCAL, "SnakeCase"),
        ("snake_c_ase", Case.SNAKE, Case.KEBAB, "snake-c-ase"),
        ("snake_c_ase", Case.SNAKE, Case.CAMEL, "snakeCAse"),
        ("snake_c_ase", Case.SNAKE, Case.PASCAL, "SnakeCAse"),
        ("kebab-case", Case.KEBAB, Case.SNAKE, "kebab_case"),
        ("kebab-case", Case.KEBAB, Case.CAMEL, "kebabCase"),
        ("kebab-case", Case.KEBAB, Case.PASCAL, "KebabCase"),
        ("kebab-c-ase", Case.KEBAB, Case.SNAKE, "kebab_c_ase"),
        ("kebab-c-ase", Case.KEBAB, Case.CAMEL, "kebabCAse"),
        ("kebab-c-ase", Case.KEBAB, Case.PASCAL, "KebabCAse"),
        ("camelCase", Case.CAMEL, Case.SNAKE, "camel_case"),
        ("camelCase", Case.CAMEL, Case.KEBAB, "camel-case"),
        ("camelCase", Case.CAMEL, Case.PASCAL, "CamelCase"),
        ("camelCAse", Case.CAMEL, Case.SNAKE, "camel_c_ase"),
        ("camelCAse", Case.CAMEL, Case.KEBAB, "camel-c-ase"),
        ("camelCAse", Case.CAMEL, Case.PASCAL, "CamelCAse"),
        ("PascalCase", Case.PASCAL, Case.SNAKE, "pascal_case"),
        ("PascalCase", Case.PASCAL, Case.KEBAB, "pascal-case"),
        ("PascalCase", Case.PASCAL, Case.CAMEL, "pascalCase"),
        ("PascalCAse", Case.PASCAL, Case.SNAKE, "pascal_c_ase"),
        ("PascalCAse", Case.PASCAL, Case.KEBAB, "pascal-c-ase"),
        ("PascalCAse", Case.PASCAL, Case.CAMEL, "pascalCAse"),
    ),
)
def test_convertor(string: str, from_case: Case, to_case: Case, result: str):
    """test case converters"""
    convert = CaseConverter.get_converter(from_case, to_case)
    assert convert(string) == result


@pytest.mark.parametrize(
    "string, from_case, to_case, result",
    (
        ("snake_case", Case.SNAKE, Case.KEBAB, "snake-case"),
        ("snakeCase", Case.SNAKE, Case.CAMEL, ValueError),
        ("kebab-case", Case.KEBAB, Case.SNAKE, "kebab_case"),
        ("kebab_case", Case.KEBAB, Case.CAMEL, ValueError),
        ("camelCase", Case.CAMEL, Case.SNAKE, "camel_case"),
        ("camel-case", Case.CAMEL, Case.KEBAB, ValueError),
        ("PascalCase", Case.PASCAL, Case.SNAKE, "pascal_case"),
        ("pascal-case", Case.PASCAL, Case.KEBAB, ValueError),
    ),
)
def test_convert_case(string: str, from_case: Case, to_case: Case, result: Any):
    """test case conversion"""
    if isinstance(result, type) and issubclass(result, Exception):
        with pytest.raises(result):
            convert_case(string, from_case, to_case)
    else:
        assert convert_case(string, from_case, to_case) == result


@pytest.mark.parametrize(
    "string, case, result",
    (
        ("normal case", Case.SNAKE, "normal_case"),
        ("normal case", Case.CAMEL, "normalCase"),
        ("normal case", Case.KEBAB, "normal-case"),
        ("normal case", Case.PASCAL, "NormalCase"),
        ("snake_case", Case.SNAKE, "snake_case"),
        ("snake_case", Case.CAMEL, "snakeCase"),
        ("snake_case", Case.KEBAB, "snake-case"),
        ("snake_case", Case.PASCAL, "SnakeCase"),
        ("camelCase", Case.SNAKE, "camel_case"),
        ("camelCase", Case.CAMEL, "camelCase"),
        ("camelCase", Case.KEBAB, "camel-case"),
        ("camelCase", Case.PASCAL, "CamelCase"),
        ("kebab-case", Case.SNAKE, "kebab_case"),
        ("kebab-case", Case.CAMEL, "kebabCase"),
        ("kebab-case", Case.KEBAB, "kebab-case"),
        ("kebab-case", Case.PASCAL, "KebabCase"),
        ("PascalCase", Case.SNAKE, "pascal_case"),
        ("PascalCase", Case.CAMEL, "pascalCase"),
        ("PascalCase", Case.KEBAB, "pascal-case"),
        ("PascalCase", Case.PASCAL, "PascalCase"),
    ),
)
def test_force_case(string: str, case: Case, result: str):
    """test case enforcing"""
    assert force_case(string, case) == result
