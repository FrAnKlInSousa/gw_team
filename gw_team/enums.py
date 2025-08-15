from enum import Enum


class UserType(str, Enum):
    admin = 'admin'
    client = 'client'
