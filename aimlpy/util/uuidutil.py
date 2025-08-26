"""
-- Created by: Ashok Kumar Pant
-- Email: asokpant@gmail.com
-- Created on: 04/05/2025
"""
import uuid


def generate_uuid() -> str:
    """
    Generate a UUID (Universally Unique Identifier) string.
    :return: A UUID string.
    """
    return str(uuid.uuid4())
