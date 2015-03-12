###############################################################################
#
# This program is part of the CiscoEnvMonE Zenpack for Zenoss.
# It is a modified version of CiscoEnvMon ZenPack which is written and
# maintained by Egor Puzanov, Copyright (C) 2010-2013
# this version is written and maintaned by Doug Syer
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
###############################################################################

from ZenPacks.community.CiscoEnvMonE.utils import decode_envmon_state
from ZODB.transact import transact
import logging
log = logging.getLogger("zen.CiscoEnvmonE")


@transact
def envmon_status_handler(device, component, evt, log=log):
    '''
    Update status properties in the model based on build in
    Zenoss status thresholds
    '''

    if not device or not component:
        return

    # prevent non min-max thresholds from triggering state change
    # and prevent tracebacks from newly discovered devices
    if not getattr(evt, 'current', None):
        return

    if not component.hasProperty('state'):
        return

    maybe_new_state = decode_envmon_state(int(float(evt.current)))

    if not getattr(component, 'state') == maybe_new_state:
        setattr(component, 'state', maybe_new_state)

    if device.zCiscoMonIgnoreNotPresent and component.state == 'notPresent':
        evt.severity = 2

    evt.summary = evt.message = "Cisco Hardware Alert, %s\
        Changed status to: %s" % (component.meta_type, maybe_new_state)


def envmon_process_threshold(device, component, evt, t_type, log=log):

    if not device or not component:
        evt.summary = 'Received temerperature alert not maping to component, its possible that the temp sensor snmp code has issues on the device'
        evt.severity = 3
        return

    if t_type == 'vHigh':
        evt.summary = evt.message = (
            "High Voltage Threshold detected, current reading is %s mv, "
            "device will shut down at %s") % (evt.current, component.voltage_threshold_high)

    elif t_type == 'vLow':
        evt.summary = evt.message = (
            "Low Voltage Threshold detected, current reading is %s mv, "
            "device will shut down at %s") % (str(evt.current), component.voltage_threshold_low)

    elif t_type == 'tHigh':
        if evt.current and float(evt.current) > 1000.0:
            evt.summary = evt.message = (
                u"Impossibly high temperature detected, current reading is %s\u00b0C "
                u"possible ios bug or faulty sensor") % str(evt.current)
            evt.severity = 4 if evt.severity != 0 else 0
        elif evt.max and evt.max == '0.0':
            evt.summary = evt.message = "Potential Cisco IOS bug temperature shut down max is not discovered"
            evt.severity = 4 if evt.severity != 0 else 0
        else:
            evt.summary = evt.message = (
                u"High temperature threshold detected, current reading is %s\u00b0C "
                u"device will shut down at %s C") % (str(evt.current), str(int(component.temperature_threshold)))
