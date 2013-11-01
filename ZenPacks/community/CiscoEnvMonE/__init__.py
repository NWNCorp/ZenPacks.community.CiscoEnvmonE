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

import logging
log = logging.getLogger("zen.CiscoEnvMon")
import Globals
import os.path
from Products.ZenModel.ZenPack import ZenPackBase
from Products.ZenRelations.RelSchema import ToManyCont, ToOne
from Products.ZenModel.DeviceHW import DeviceHW
from Products.ZenUtils.Utils import unused
from Products.ZenRelations.zPropertyCategory import setzPropertyCategory
from Products.Zuul.interfaces import ICatalogTool

unused(Globals)

productNames = (
    'CiscoEnvMonFan',
    'CiscoEnvMonTemperatureSensor',
    'CiscoEnvMonVoltageSensor',
    'CiscoEnvMonPowerSupply',
    )


skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
from Products.CMFCore.DirectoryView import registerDirectory
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())

# add new type of hardware relation so we can access
# in the model via dev.hw.xxx
DeviceHW._relations += (("ciscoenvvoltagesensors", ToManyCont(
    ToOne, "ZenPacks.community.CiscoEnvMonE.CiscoEnvMonVoltageSensor", "hw")), )
DeviceHW._relations += (("ciscoenvtempsensors", ToManyCont(
    ToOne, "ZenPacks.community.CiscoEnvMonE.CiscoEnvMonTemperatureSensor", "hw")), )
DeviceHW._relations += (("ciscoenvfans", ToManyCont(
    ToOne, "ZenPacks.community.CiscoEnvMonE.CiscoEnvMonFan", "hw")), )
DeviceHW._relations += (("ciscoenvpowersupplies", ToManyCont(
    ToOne, "ZenPacks.community.CiscoEnvMonE.CiscoEnvMonPowerSupply", "hw")), )


class ZenPack(ZenPackBase):

    # setting zCiscoMonIgnoreNotPresent will drop alerts from components in the
    # notPresent state
    # setting zCiscoMonTemperatureFactor will set temperaturealert thresholds
    # to be shutdown temp threshold - zCiscoMonTemperatureFactor (in celcius)
    # zCiscoMonVoltageFactor works the same way (millivolts)
    # note -2 temperature factore is about 4F

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

    def upgrade(self, app):

        ZenPackBase.upgrade(self, app)
        self._buildHWRelations()

    def remove(self, app, leaveObjects=False):
        if not leaveObjects:

            NEW_COMPONENT_TYPES = tuple([x for x in productNames])

            log.info('Removing ZenPacks.community.CiscoEnvmonE components')
            cat = ICatalogTool(app.zport.dmd)

            # Search the catalog for components of this zenpacks type.
            if NEW_COMPONENT_TYPES:
                for brain in cat.search(types=NEW_COMPONENT_TYPES):
                    component = brain.getObject()
                    component.getPrimaryParent()._delObject(component.id)

            # remote HW component relations
            DeviceHW._relations = tuple(
                [x for x in DeviceHW._relations if x[0] != 'voltagesensors'])

            log.info('Removing ZenPacks.community.CiscoEnvMonE \
                relationships from existing devices')

            self._buildHWRelations()

        super(ZenPack, self).remove(app, leaveObjects=leaveObjects)

    def _buildHWRelations(self):
        for d in self.dmd.Devices.getSubDevicesGen():
            d.hw.buildRelations()
            d.buildRelations()
