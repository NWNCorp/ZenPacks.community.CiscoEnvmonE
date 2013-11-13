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

__doc__ = """CiscoEnvMonVoltageSensorMap

CiscoVoltageSensorMap maps the ciscoEnvMonVoltageStatusTable table to
voltage sensor objects

"""

__version__ = '$Revision: 1.1 $'[11:-2]

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap
from ZenPacks.community.CiscoEnvMonE.utils import decode_envmon_state, match_exclude_regex


class CiscoEnvMonVoltageSensorMap(SnmpPlugin):
    """Map Cisco voltage Sensors table to model."""

    maptype = "CiscoEnvMonVoltageSensorMap"
    modname = "ZenPacks.community.CiscoEnvMonE.CiscoEnvMonVoltageSensor"
    relname = "ciscoenvvoltagesensors"
    compname = "hw"
    deviceProperties = SnmpPlugin.deviceProperties + ('zEnvMonMapIgnoreNames',)

    snmpGetTableMaps = (
        GetTableMap('VoltageStatusTable',
                    '.1.3.6.1.4.1.9.9.13.1.2.1',
                    {
                        '.2': 'title',
                        '.7': 'state',
                        '.4': 'voltage_threshold_low',
                        '.5': 'voltage_threshold_high',
                        '.6': 'voltage_last_shutdown'
                    }), )

    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        v_tbl = results[1].get('VoltageStatusTable', {})

        # if no no comps found exit
        if not v_tbl:
            log.info('%s NOT found on device %s ---- skipping Model' % (self.relname, device.id))
            return None

        rm = self.relMap()

        for snmpindex, row in v_tbl.items():
            om = self.objectMap(row)

            # there are IOS bugs out there where sensors will not get names
            # guard against this condition
            if om.title == '':
                om.title = 'Unknown-(probable IOS bug)'

            if match_exclude_regex(device, om.title, self.maptype, log):
                continue

            om.title = om.title.strip(' in mV')
            om.id = self.prepId(om.title)
            om.state = decode_envmon_state(om.state)
            om.snmpindex = snmpindex.strip('.')
            rm.append(om)
        return rm
