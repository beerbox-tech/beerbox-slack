"""
created by: Thibault DEFEYTER
created at: 2022/11/29
license: MIT

slackbox api base component
"""

from pydantic import BaseModel
from pydantic import Extra

from slackbox.utils.strings import Case
from slackbox.utils.strings import force_case


class APIComponent(BaseModel):
    """base component for all API components"""

    class Config:
        """config to be shared across all API components"""

        allow_population_by_field_name = True
        extra = Extra.forbid

        @classmethod
        def alias_generator(cls, string: str) -> str:
            """automatique alias generator for all component's fields"""
            return force_case(string, case=Case.CAMEL)
