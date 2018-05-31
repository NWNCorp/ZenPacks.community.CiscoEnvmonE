"""
CiscoPowerSupplyMap maps the ciscoEnvMonTemperatureStatusTable table to power supply objects
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
from ZenPacks.community.CiscoEnvMonE.utils import (
    decode_envmon_state,
    decode_ps_source,
    match_exclude_regex
)


class CiscoEnvMonPowerSupplyMap(SnmpPlugin):
    """Map Cisco Environment PowerSupplys table to model."""

    maptype = "CiscoEnvMonPowerSupplyMap"
    modname = "ZenPacks.community.CiscoEnvMonE.CiscoEnvMonPowerSupply"
    relname = "ciscoenvpowersupplies"
    compname = "hw"
    deviceProperties = SnmpPlugin.deviceProperties + ('zEnvMonMapIgnoreNames',)

    snmpGetTableMaps = (
        GetTableMap('PowerSupplyTable',
                    '.1.3.6.1.4.1.9.9.13.1.5.1',
                    {
                        '.2': 'title',
                        '.3': 'state',
                        '.4': 'supply_source',
                    }), )

    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)

        p_tbl = results[1].get('PowerSupplyTable', {})

        # if no no comps found exit
        if not p_tbl:
            log.info('%s NOT found on device %s ---- skipping Model' % (self.relname, device.id))
            return None

        rm = self.relMap()

        for snmpindex, row in p_tbl.items():
            om = self.objectMap(row)

            # there are IOS bugs out there where sensors will not get names
            # guard against this condition
            if om.title == '':
                om.title = 'Unknown-(probable IOS bug)'

            if match_exclude_regex(device, om.title, self.maptype, log):
                continue

            if hasattr(om, 'supply_source'):
                om.supply_source = decode_ps_source(om.supply_source)
            else:
                om.supply_source = "Not Reported"
                om.snmpindex = snmpindex.strip('.')

            om.id = self.prepId(om.title)
            om.state = decode_envmon_state(om.state)
            om.snmpindex = snmpindex.strip('.')
            rm.append(om)

        if rm.maps:
            log.info('Found %d CiscoEnvMonPowerSupplies' % len(rm.maps))
        else:
            log.info('No CiscoEnvMonFans Found')

        return rm
