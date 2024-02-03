from env import *
from utils import ReExp

_access_denied_finding_property = ReExp('Access denied finding property "%s"')

def func(env:Env, log):

    #01-28 01:07:15.510 25414  8551 W libc    : Access denied finding property "vendor.vivo.imageencoder.dump"
    #01-28 01:07:15.513 25414  8600 W libc    : Access denied finding property "vendor.vivo.debug.PqSetting.enable"
    if _access_denied_finding_property.match(log.msg):
        env.state_set("property", _access_denied_finding_property.get(0))
