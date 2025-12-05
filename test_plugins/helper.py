from jinja2 import Undefined
import ipaddress
import re

from ansible.template import accept_args_markers

@accept_args_markers
def is_present(value):
    """ Return true if the value is defined and not empty or blank or None.
     
        Note that a value of False is 'present'. It is a value.      
        """
    if isinstance(value, Undefined): return False
    if value is None: return False
    if isinstance(value, (str)): return bool(value.strip())
    if isinstance(value, (str, list, dict, set)): return bool(value)
    return True

@accept_args_markers
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
        if not is_netmask(net): return False
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

_RE_HOSTNAME = re.compile("^(?!-)[a-z0-9-]{1,63}(?<!-)$")
_RE_FQDN     = re.compile("^((?!-)[a-z0-9-]{1,63}(?<!-)\.)+([a-z]{2,63})$")

def is_hostname(value):
    """ Check if value is a valid hostname (letters, digits, dashes, no dots). """
    if not isinstance(value, str): return False
    if 1 > len(value) > 255: return False
    return _RE_HOSTNAME.match(value) is not None

def is_fqdn(value):
    """ Check if value is a fully qualified domain name. """
    if not isinstance(value, str): return False
    if 1 > len(value) > 255: return False
    return _RE_FQDN.match(value) is not None

class TestModule:
    def tests(self):
        return {
            name[3:]: value
            for name, value in globals().items()
            if name.startswith('is_') and hasattr(value, '__call__')
        }