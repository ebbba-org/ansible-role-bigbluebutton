from jinja2 import Undefined
import ipaddress
import re

def filter_strformat(value, format="%s"):
    return format % value

class FilterModule:
    def filters(self):
        return {
            name[7:]: value
            for name, value in globals().items()
            if name.startswith('filter_') and hasattr(value, '__call__')
        }