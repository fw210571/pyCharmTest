import os
from enum import Enum
from enum import unique

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class BaseEnumClass(Enum):
    @classmethod
    def has_value(cls, value):
        return value in [e[0] for e in cls._value2member_map_]

@unique
class ClientEnum(BaseEnumClass):
    LEVELUP = ("LEVELUP")



@unique
class ClientNameEnum(BaseEnumClass):
    levelup = "levelup"


@unique
class LoggingLevelEnum(BaseEnumClass):
    DEBUG = ("DEBUG",)
    INFO = ("INFO",)
    WARNING = ("WARNING",)
    ERROR = ("ERROR",)


@unique
class BrowserEnum(BaseEnumClass):
    CHROME = ("chrome",)
    EDGE = ("edge",)
    FIREFOX = ("firefox",)
    SAFARI = ("safari",)


@unique
class EnvironmentEnum(BaseEnumClass):
    PRODUCTION = ("production",)
    RELEASE = ("release",)
    STAGE1 = ("stage1",)
