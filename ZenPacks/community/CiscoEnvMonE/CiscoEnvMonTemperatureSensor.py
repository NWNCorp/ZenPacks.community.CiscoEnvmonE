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

__doc__ = """CiscoEnvMonTemperatureSensor

CiscoEnvmonTemperatureSensor is a class describing a temperature sensor as defined in the
CiscoEnvmon Mib.

"""

__version__ = "$Revision: 2.0 $"[11:-2]

import logging
log = logging.getLogger("zen.CiscoEnvMonE")
from Globals import InitializeClass
from Products.ZenModel.HWComponent import HWComponent
from Products.ZenModel.TemperatureSensor import TemperatureSensor
from Products.ZenRelations.RelSchema import ToManyCont, ToOne
from Products.Zuul.infos.component import ComponentInfo
from Products.Zuul.interfaces.component import IComponentInfo
from sys import maxint
from zope.interface import implements
from Products.Zuul.form import schema
from Products.Zuul.infos import ProxyProperty
from Products.Zuul.utils import ZuulMessageFactory as _t
from Products.ZenModel.ZenossSecurity import ZEN_CHANGE_DEVICE


class CiscoEnvMonTemperatureSensor(TemperatureSensor):
    """Cisco TemperatureSensor object"""

    portal_type = meta_type = 'CiscoEnvMonTemperatureSensor'

    temperature_threshold = ''
    temperature_last_shutdown = ''
    state = 'Unknown'

    _properties = TemperatureSensor._properties + (
        {'id': 'temperature_threshold', 'type': 'string'},
        {'id': 'temperature_last_shutdown', 'type': 'string'},
        )

    _relations = HWComponent._relations + (
        ("hw", ToOne(ToManyCont, "Products.ZenModel.DeviceHW", "ciscoenvtempsensors")),
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

    @property
    def temp_threshold_string(self):
        tc = self.temperature_threshold or 'Unknown'
        if tc == 'Unknown':
            return 'Not Available'
        tf = str(self.getTempFahrenheit(tc))
        return u"%s \u00b0C / %s F" % (tc, tf)

    @property
    def temp_lastshutdown_string(self):
        tc = self.temperature_last_shutdown or 'Unknown'
        if tc == 'Unknown':
            return 'Not Available'
        tf = self.getTempFahrenheit(tc)
        return "%s \u00b0C / %s \u00b0F" % (tc, tf)

    @property
    def sensor_temperature_threshold(self):
        if self.temperature_threshold == '':
            return maxint
        else:
            return float(self.temperature_threshold)

    def getTempFahrenheit(self, temp_C):
        """
        Return the degrees fahrenheit given degrees Celcius
        """
        if temp_C is not None:
            temp_F = int(temp_C) * 9 / 5 + 32
            return long(temp_F)
        return None


class ICiscoEnvMonTemperatureSensorInfo(IComponentInfo):
    temp_threshold_string = schema.TextLine(title=_t(u'Temperature threshold'))
    temp_lastshutdown_string = schema.TextLine(title=_t(u'Temperature at last emergency \
        thermal shutdown'))


class CiscoEnvMonTemperatureSensorInfo(ComponentInfo):
    implements(ICiscoEnvMonTemperatureSensorInfo)

    temp_threshold_string = ProxyProperty('temp_threshold_string')
    temp_lastshutdown_string = ProxyProperty('temp_lastshutdown_string')

    # override the default status method to show component-specific status
    @property
    def status(self):
        ts_state = self._object.state
        if ts_state:
            return self._object.state
        else:
            return 'Unknown'

InitializeClass(CiscoEnvMonTemperatureSensor)
