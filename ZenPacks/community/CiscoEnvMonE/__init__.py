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


""" Zenpack Loader and installer """

import Globals
import logging
from Products.ZenUtils.Utils import unused
from Products.Zuul.interfaces import ICatalogTool
from Products.ZenRelations.zPropertyCategory import setzPropertyCategory
from Products.ZenModel.ZenPack import ZenPackBase

log = logging.getLogger("zen.CiscoEnvMon")
unused(Globals)

import ZenPacks.community.CiscoEnvMonE.patches

productNames = (
    'CiscoEnvMonFan',
    'CiscoEnvMonTemperatureSensor',
    'CiscoEnvMonVoltageSensor',
    'CiscoEnvMonPowerSupply',
    )

class ZenPack(ZenPackBase):
    """ zenpack installer

    setting zCiscoMonIgnoreNotPresent will drop alerts from components in the
    notPresent state
    setting zCiscoMonTemperatureFactor will set temperaturealert thresholds
    to be shutdown temp threshold - zCiscoMonTemperatureFactor (in celcius)
    zCiscoMonVoltageFactor works the same way (millivolts)
        note -2 temperature factore is about 4F
    """

    packZProperties = [
        ('zCiscoMonIgnoreNotPresent', True, 'boolean'),
        ('zCiscoMonTemperatureFactor', .90, 'float'),
        ('zCiscoMonVoltageFactor', .90, 'float'),
        ('zEnvMonMapIgnoreNames', '', 'string'),
        ]

    for i in packZProperties:
        setzPropertyCategory(i[0], "CiscoEnvMonE")

    def install(self, app):
        ZenPackBase.install(self, app)

        super(ZenPack, self).install(app)
        log.info("Adding ZenPacks.community.CiscoEnvmonE"
                 " relationships to existing devices")

        self._buildHWRelations()

    def remove(self, app, leaveObjects=False):
        if not leaveObjects:

            from Products.ZenModel.DeviceHW import DeviceHW

            NEW_COMPONENT_TYPES = tuple([x for x in productNames])

            log.info('Removing ZenPacks.community.CiscoEnvmonE components')
            cat = ICatalogTool(app.zport.dmd)

            # Search the catalog for components of this zenpacks type.
            if NEW_COMPONENT_TYPES:
                for brain in cat.search(types=NEW_COMPONENT_TYPES):
                    component = brain.getObject()
                    component.getPrimaryParent()._delObject(component.id)

            hw_relations = (
                "ciscoenvvoltagesensors",
                "ciscoenvtempsensors"
                "ciscoenvfans"
                "ciscoenvpowersupplies"
            )

            # remote HW component relations
            DeviceHW._relations = tuple(
                [x for x in DeviceHW._relations if x[0] not in hw_relations])

            log.info('Removing ZenPacks.community.CiscoEnvMonE'
                     'relationships from existing devices')

            self._buildHWRelations()

        super(ZenPack, self).remove(app, leaveObjects=leaveObjects)

    def _buildHWRelations(self):
        for d in self.dmd.Devices.getSubDevicesGen():
            d.hw.buildRelations()
            d.buildRelations()
