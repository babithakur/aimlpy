"""
-- Created by: Ashok Kumar Pant
-- Email: asokpant@gmail.com
-- Created on: 04/05/2025
"""


def is_empty(string: str) -> bool:
    return string is None or string == ''


def is_not_empty(string: str) -> bool:
    return not is_empty(string)
