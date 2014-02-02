import ConfigParser
import hashlib

_config = ConfigParser.RawConfigParser()
_config.read("/home/ec2-user/fldb/password.cfg")
_salt = _config.get('Auth', 'salt')

def hash(password):
    m = hashlib.md5()
    m.update(self.password + _salt)
    return m.hexdigest()
