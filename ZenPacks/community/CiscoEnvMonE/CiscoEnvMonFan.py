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

"""
This module provides Monitoring Functionality for Cisco EnvMonFan Objects
"""

import logging
from zope.interface import implements
from Products.ZenModel.ZenossSecurity import ZEN_CHANGE_DEVICE
from Products.ZenModel.Fan import Fan
from Products.ZenModel.HWComponent import HWComponent
from Products.ZenRelations.RelSchema import ToManyCont, ToOne
from Products.Zuul.infos.component import ComponentInfo
from Products.Zuul.interfaces.component import IComponentInfo

log = logging.getLogger("zen.CiscoEnvMon")


class CiscoEnvMonFan(Fan):
    """Cisco Fan object monitored via the Cisco Envmon Mib"""

    portal_type = meta_type = 'CiscoEnvMonFan'

    state = 'Unknown'

    _relations = HWComponent._relations + (
        ("hw", ToOne(ToManyCont, "Products.ZenModel.DeviceHW", "ciscoenvfans")),
        )

    factory_type_information = ({
        'actions': ({
            'id': 'perfConf',
            'name': 'Template',
            'action': 'objTemplates',
            'permissions': (ZEN_CHANGE_DEVICE, )
            }, )
        }, )


class ICiscoEnvMonFanInfo(IComponentInfo):
    """ CiscoEnvMonFan Interface """
    pass


class CiscoEnvMonFanInfo(ComponentInfo):
    """ CiscoEnvMonFan Info Adapter """
    implements(ICiscoEnvMonFanInfo)

    @property
    def status(self):
        """override the default status method to show component-specific status"""
        fan_state = self._object.state
        if fan_state:
            return self._object.state

        return 'Unknown'
