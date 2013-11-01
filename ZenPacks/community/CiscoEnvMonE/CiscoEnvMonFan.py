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

__doc__ = """CiscoEnvMonFan

CiscoEnvmonFan is a class describing a fan as defined in the
CiscoEnvmon Mib.

"""

__version__ = "$Revision: 2.0 $"[11:-2]

import logging
log = logging.getLogger("zen.CiscoEnvMon")
from Globals import InitializeClass
from Products.ZenModel.Fan import Fan
from Products.ZenModel.HWComponent import HWComponent
from Products.ZenRelations.RelSchema import ToManyCont, ToOne
from Products.Zuul.infos.component import ComponentInfo
from Products.Zuul.interfaces.component import IComponentInfo
from zope.interface import implements
from Products.Zuul.form import schema
from Products.Zuul.infos import ProxyProperty
from Products.Zuul.utils import ZuulMessageFactory as _t


class CiscoEnvMonFan(Fan):
    """Cisco Fan object"""

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
            'permissions': ('ZEN_CHANGE_DEVICE',)
            }, )
        }, )

    def manage_deleteComponent(self, REQUEST=None):
        """
        Delete Component
        """
        self.getPrimaryParent()._delObject(self.id)
        if REQUEST is not None:
            REQUEST['RESPONSE'].redirect(self.device().hw.absolute_url())


class ICiscoEnvMonFanInfo(IComponentInfo):
    pass


class CiscoEnvMonFanInfo(ComponentInfo):
    implements(ICiscoEnvMonFanInfo)

    # override the default status method to show component-specific status
    @property
    def status(self):
        fan_state = self._object.state
        if fan_state:
            return self._object.state
        else:
            return 'Unknown'

InitializeClass(CiscoEnvMonFan)
