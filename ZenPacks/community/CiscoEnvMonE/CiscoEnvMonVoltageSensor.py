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

__doc__ = """CiscoEnvMonVoltageSensor

CiscoEnvmonVoltageSensor is a class describing a voltage sensor as defined in the
CiscoEnvmon Mib.

"""

__version__ = "$Revision: 1.0 $"[11:-2]

import logging
log = logging.getLogger("zen.CiscoEnvMon")
from Globals import InitializeClass
from Products.ZenModel.HWComponent import HWComponent
from Products.ZenRelations.RelSchema import ToManyCont, ToOne
from sys import maxint
from Products.Zuul.infos.component import ComponentInfo
from Products.Zuul.interfaces.component import IComponentInfo
from zope.interface import implements
from Products.Zuul.form import schema
from Products.Zuul.infos import ProxyProperty
from Products.Zuul.utils import ZuulMessageFactory as _t
from Products.ZenModel.ZenossSecurity import ZEN_CHANGE_DEVICE
from Products.ZenUtils.Utils import convToUnits


class CiscoEnvMonVoltageSensor(HWComponent):
    """Cisco Voltage Sensor object"""

    portal_type = meta_type = 'CiscoEnvMonVoltageSensor'

    voltage_threshold_low = maxint
    voltage_threshold_high = -maxint-1
    voltage_last_shutdown = ''
    state = ''

    _properties = HWComponent._properties + (
        {'id': 'voltage_threshold_low', 'type': 'string'},
        {'id': 'voltage_threshold_high', 'type': 'string'},
        {'id': 'voltage_last_shutdown', 'type': 'string'},
        {'id': 'state', 'type': 'string'}
        )

    _relations = HWComponent._relations + (
        ("hw", ToOne(ToManyCont, "Products.ZenModel.DeviceHW", "ciscoenvvoltagesensors")),
        )

    factory_type_information = ({
        'actions': ({
            'id': 'perfConf',
            'name': 'Template',
            'action': 'objTemplates',
            'permissions': ('ZEN_CHANGE_DEVICE',)
            }, )
        }, )

    def device(self):
        hw = self.hw()
        if hw:
            return hw.device()

    def manage_deleteComponent(self, REQUEST=None):
        """Delete Component"""
        self.getPrimaryParent()._delObject(self.id)
        if REQUEST is not None:
            REQUEST['RESPONSE'].redirect(self.device().hw.absolute_url())

    @property
    def low_voltage_threshold(self):
        """ return low voltage property as float setting for use in thresholding """
        if self.voltage_threshold_low == '':
            return -maxint-1
        else:
            return float(self.voltage_threshold_low)

    @property
    def high_voltage_threshold(self):
        """ high voltage shutdown property as float to be used for threhsolding """
        if self.voltage_threshold_high == '':
            return maxint
        else:
            return float(self.voltage_threshold_high)

    def getMillivoltsString(self, mv):
        """Return millivolts as a string to be used in gui"""
        if mv == '':
            return 'Not Reported'
        return " %s mv" % "{:,}".format(int(mv))

    @property
    def combined_shutdown_thresholds_string(self):
        return "%s/%s" % (self.lv_threshold_string, self.hv_threshold_string)

    @property
    def lv_threshold_string(self):
        return str(self.getMillivoltsString(self.voltage_threshold_low))

    @property
    def hv_threshold_string(self):
        return str(self.getMillivoltsString(self.voltage_threshold_high))

    @property
    def voltage_last_shutdown_string(self):
        return str(self.getMillivoltsString(self.voltage_last_shutdown))


class ICiscoEnvMonVoltageSensorInfo(IComponentInfo):
    lv_threshold_string = schema.TextLine(title=_t(u'Low Voltage Shutdown Threshold'))
    voltage_threshold_high = schema.TextLine(title=_t(u'High Voltage Shutdown Threshold'))
    voltage_last_shutdown = schema.TextLine(title=_t(u'Voltage reading at last \
        emergency shutdown'))
    state = schema.TextLine(title=_t(u'current state'))


class CiscoEnvMonVoltageSensorInfo(ComponentInfo):
    implements(ICiscoEnvMonVoltageSensorInfo)

    combined_shutdown_thresholds_string = ProxyProperty('combined_shutdown_thresholds_string')
    voltage_threshold_low = ProxyProperty('lv_threshold_string')
    voltage_threshold_high = ProxyProperty('hv_threshold_string')
    voltage_last_shutdown = ProxyProperty('voltage_last_shutdown_string')
    state = ProxyProperty('state')

    # override the default status method to show component-specific status
    @property
    def status(self):
        voltage_state = self._object.state
        if voltage_state:
            return self._object.state
        else:
            return 'Unknown'

InitializeClass(CiscoEnvMonVoltageSensor)
