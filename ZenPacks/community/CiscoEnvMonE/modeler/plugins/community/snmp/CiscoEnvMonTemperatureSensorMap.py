"""
CiscoEnvMonTemperatureSensorMap maps the ciscoEnvMonTemperatureStatusTable table to temperature sensor objects
"""

################################################################################
#
# This program is part of the CiscoEnvMonE Zenpack for Zenoss.
# It is a modified version of CiscoEnvMon ZenPack which is written and
# maintained by Egor Puzanov, Copyright (C) 2010-2013
# Thanks for your excellent Zenpacks Egor!
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################


from sys import maxint
import re
from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap
from ZenPacks.community.CiscoEnvMonE.utils import decode_envmon_state, match_exclude_regex

class CiscoEnvMonTemperatureSensorMap(SnmpPlugin):
    """Map Cisco Environment Temperature Sensors table to model."""

    maptype = "CiscoEnvMonTemperatureSensorMap"
    modname = "ZenPacks.community.CiscoEnvMonE.CiscoEnvMonTemperatureSensor"
    relname = "ciscoenvtempsensors"
    compname = "hw"
    deviceProperties = SnmpPlugin.deviceProperties + ('zEnvMonMapIgnoreNames',)

    snmpGetTableMaps = (
        GetTableMap('TemperatureTable',
                    '.1.3.6.1.4.1.9.9.13.1.3.1',
                    {
                        '.2': 'title',
                        '.4': 'temperature_threshold',
                        '.5': 'temperature_last_shutdown',
                        '.6': 'state'
                    }), )

    def process(self, device, results, log):
        """collect snmp information from this device"""

        log.info('processing %s for device %s', self.name(), device.id)

        # if no no comps found exit
        t_tbl = results[1].get('TemperatureTable', {})
        if not t_tbl:
            log.info('%s NOT found on device %s ---- skipping Model' % (self.relname, device.id))
            return None

        rm = self.relMap()

        for snmpindex, row in t_tbl.items():
            om = self.objectMap(row)

            # there are IOS bugs out there where sensors will not get names
            # guard against this condition
            if om.title == '':
                om.title = 'Unknown-(probable IOS bug)'
                log.info('Not getting temperature sensor names correctly, may be IOS bug')

            # for some reason Cisco appends the current status to the name of the component
            # strip this off as is makes attaching traps etc very difficult
            om.title = re.sub(r', (RED|YELLOW|GREEN)$', '', om.title)
            om.title = om.title.rstrip(', YELLOW').rstrip(', RED').rstrip(', GREEN')

            if match_exclude_regex(device, om.title, self.maptype, log):
                continue

            om.id = self.prepId(om.title)
            om.state = decode_envmon_state(om.state)
            om.snmpindex = snmpindex.strip('.')

            # you can get some crazy values for this...do a sanity check
            ts = getattr(om, 'temperature_threshold', '')
            if not ts or ts <= 0 or ts >= 750:
                om.temperature_threshold = str(maxint/2)

            rm.append(om)

        if rm.maps:
            log.info('Found %d CiscoEnvMonTemperaturSensors' % len(rm.maps))
        else:
            log.info('No CiscoEnvMonTemperaturSensors Found')

        return rm
