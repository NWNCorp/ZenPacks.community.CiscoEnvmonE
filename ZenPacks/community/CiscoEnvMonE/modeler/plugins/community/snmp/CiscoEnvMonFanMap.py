"""
CiscoFanMap maps the ciscoEnvMonTemperatureStatusTable table to temperaturesensors objects
"""

################################################################################
#
# This program is part of the CiscoEnvMonE Zenpack for Zenoss.
# It is a modified version of CiscoEnvMon ZenPack which is written and
# maintained by Egor Puzanov, Copyright (C) 2010-2013
# this version is written and maintaned by Doug Syer
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################


from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap
from ZenPacks.community.CiscoEnvMonE.utils import decode_envmon_state, match_exclude_regex


class CiscoEnvMonFanMap(SnmpPlugin):
    """Map Cisco Environment Fans table to model."""

    maptype = "CiscoEnvMonFanMap"
    modname = "ZenPacks.community.CiscoEnvMonE.CiscoEnvMonFan"
    relname = "ciscoenvfans"
    compname = "hw"
    deviceProperties = SnmpPlugin.deviceProperties + ('zEnvMonMapIgnoreNames',)

    snmpGetTableMaps = (
        GetTableMap('FanTable',
                    '.1.3.6.1.4.1.9.9.13.1.4.1',
                    {
                        '.2': 'title',
                        '.3': 'state',
                    }), )

    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)

        f_tbl = results[1].get('FanTable', {})

        # if no no comps found exit
        if not f_tbl:
            log.info('%s NOT found on device %s ---- skipping Model' % (self.relname, device.id))
            return None

        rm = self.relMap()

        for snmpindex, row in f_tbl.items():
            om = self.objectMap(row)

            # there are IOS bugs out there where sensors will not get names
            # guard against this condition
            if om.title == '':
                om.title = 'Unknown-(probable IOS bug)'

            if match_exclude_regex(device, om.title, self.maptype, log):
                continue

            om.id = self.prepId(om.title)
            om.state = decode_envmon_state(om.state)
            om.snmpindex = snmpindex.strip('.')
            rm.append(om)

        if rm.maps:
            log.info('Found %d CiscoEnvMonFans' % len(rm.maps))
        else:
            log.info('No CiscoEnvMonFans Found')

        return rm
