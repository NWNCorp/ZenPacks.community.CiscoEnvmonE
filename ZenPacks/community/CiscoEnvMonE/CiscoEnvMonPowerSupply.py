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
This module provides Monitoring Functionality for Cisco CiscoEnvMonPowerSupplyObjects
"""
import logging
from zope.interface import implements
from Products.ZenModel.ZenossSecurity import ZEN_CHANGE_DEVICE
from Products.ZenModel.HWComponent import HWComponent
from Products.ZenModel.PowerSupply import PowerSupply
from Products.ZenRelations.RelSchema import ToManyCont, ToOne
from Products.Zuul.interfaces.component import IComponentInfo
from Products.Zuul.form import schema
from Products.Zuul.infos import ProxyProperty
from Products.Zuul.infos.component import ComponentInfo
from Products.Zuul.utils import ZuulMessageFactory as _t

log = logging.getLogger("zen.CiscoEnvMon")


class CiscoEnvMonPowerSupply(PowerSupply):
    """Cisco Power Supply object monitored via the Cisco Envmon Mib"""


    portal_type = meta_type = 'CiscoEnvMonPowerSupply'

    state = 'Unknown'
    supply_source = 'Unknown'

    _properties = PowerSupply._properties + (
        {'id': 'supply_source', 'type': 'string'},
        )

    _relations = HWComponent._relations + (
        ("hw", ToOne(ToManyCont, "Products.ZenModel.DeviceHW", "ciscoenvpowersupplies")),
        )

    factory_type_information = ({
        'actions': ({
            'id': 'perfConf',
            'name': 'Template',
            'action': 'objTemplates',
            'permissions': (ZEN_CHANGE_DEVICE,)
            }, )
        }, )


class ICiscoEnvMonPowerSupplyInfo(IComponentInfo):
    """ CiscoEnvMonPowerSupply Interface """
    supply_source = schema.TextLine(title=_t(u'Power supply source'))


class CiscoEnvMonPowerSupplyInfo(ComponentInfo):
    """ CiscoEnvMonPowerSupply Info Adapter """
    implements(ICiscoEnvMonPowerSupplyInfo)

    supply_source = ProxyProperty('supply_source')

    # override the default status method to show component-specific status
    @property
    def status(self):
        fan_state = self._object.state
        if fan_state:
            return self._object.state

        return 'Unknown'
