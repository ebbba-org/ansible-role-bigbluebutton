from jinja2 import Undefined
import ipaddress
import re

def is_present(value):
    """ Return true if the value is defined and not empty or blank. """
    if isinstance(value, Undefined): return False
    if isinstance(value, (str)): return bool(value.strip())
    if isinstance(value, (str, list, dict, set)): return bool(value)
    return True

def is_missing(value):
    """ Return true if the value is undefined, None or an empty or blank string. """
    if isinstance(value, Undefined): return True
    if value is None: return True
    if isinstance(value, str): return not bool(value.strip())
    return False

def is_ip(value, v=None, private=None, public=None, loopback=None, local=None, net=None):
    if not isinstance(value, str): return False
    try:
        ip = ipaddress.ip_address(value)
    except ValueError:
        return False
    if v and ip.version != v: return False
    if private is not None  and ip.is_private    is not private: return False
    if public is not None   and ip.is_global     is not public: return False
    if loopback is not None and ip.is_loopback   is not loopback: return False
    if local is not None    and ip.is_link_local is not local: return False
    if net:
        if not is_net(net): return False
        if ip not in ipaddress.ip_network(net): return False
    return True

def is_netmask(value, v=None, private=None, public=None, loopback=None, local=None):
    if not isinstance(value, str): return False
    try:
        net = ipaddress.ip_network(value)
    except ValueError:
        return False
    if v and net.version != v: return False
    if private is not None  and net.is_private    is not private: return False
    if public is not None   and net.is_global     is not public: return False
    if loopback is not None and net.is_loopback   is not loopback: return False
    if local is not None    and net.is_link_local is not local: return False
    return True

_RE_FQDN_PART = re.compile("(?!-)[a-z\\d-]{1,63}(?<!-)$")

def is_hostname(value):
    if not isinstance(value, str): return False
    if 1 > len(value) > 255: return False
    return all(map(_RE_FQDN_PART.match, value.split(".")))

def is_fqdn(value):
    return is_hostname(value) and '.' in value

class TestModule:
    def tests(self):
        return {
            name[3:]: value
            for name, value in globals().items()
            if name.startswith('is_') and hasattr(value, '__call__')
        }