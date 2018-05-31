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
This module provides Monitoring Functionality for Cisco CiscoEnvMonVoltageSensor Objects
"""

from sys import maxint
import logging

from zope.interface import implements
from Products.ZenModel.HWComponent import HWComponent
from Products.ZenModel.ZenossSecurity import ZEN_CHANGE_DEVICE
from Products.ZenRelations.RelSchema import ToManyCont, ToOne
from Products.Zuul.infos.component import ComponentInfo
from Products.Zuul.interfaces.component import IComponentInfo
from Products.Zuul.form import schema
from Products.Zuul.infos import ProxyProperty
from Products.Zuul.utils import ZuulMessageFactory as _t

log = logging.getLogger("zen.CiscoEnvMon")


class CiscoEnvMonVoltageSensor(HWComponent):
    """Cisco CiscoEnvMonVoltageSensor object  monitored via the Cisco Envmon Mib"""

    MAX_VOLTAGE = maxint / 2
    MIN_VOLTAGE = (-maxint - 1) / 2

    portal_type = meta_type = 'CiscoEnvMonVoltageSensor'

    voltage_threshold_low = MAX_VOLTAGE
    voltage_threshold_high = MIN_VOLTAGE
    voltage_last_shutdown = ''
    state = 'Unknown'

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
            'permissions': (ZEN_CHANGE_DEVICE, )
            }, )
        }, )

    def device(self):
        """ required for all components path back to the device """
        hw = self.hw()
        if hw:
            return hw.device()

    def getMillivoltsString(self, mv):
        """Return millivolts as a string to be used in gui"""

        if mv == '':
            return 'Not Reported'

        return " %s mv" % "{:,}".format(int(mv))

    @property
    def combined_shutdown_thresholds_string(self):
        """ displays low and high voltage shut down thresholds """
        return "%s/%s" % (self.lv_threshold_string, self.hv_threshold_string)

    @property
    def lv_threshold_string(self):
        """ returns low voltage threshold """
        lvt = self.voltage_threshold_low
        if lvt == str(self.MIN_VOLTAGE):
            return "Not Provided"
        return str(self.getMillivoltsString(lvt))

    @property
    def hv_threshold_string(self):
        """ return high voltage threshold """
        hvt = self.voltage_threshold_high
        if hvt == str(self.MAX_VOLTAGE):
            return "Not Provided"
        return str(self.getMillivoltsString(hvt))

    @property
    def voltage_last_shutdown_string(self):
        """ provide last shutdown voltage """
        return str(self.getMillivoltsString(self.voltage_last_shutdown))


class ICiscoEnvMonVoltageSensorInfo(IComponentInfo):
    """ CiscoEnvMonVoltageSenso Interface """

    lv_threshold_string = schema.TextLine(title=_t(u'Low Voltage Shutdown Threshold'))
    voltage_threshold_high = schema.TextLine(title=_t(u'High Voltage Shutdown Threshold'))
    voltage_last_shutdown = schema.TextLine(title=_t(u'Voltage reading at last emergency shutdown'))


class CiscoEnvMonVoltageSensorInfo(ComponentInfo):
    """ CiscoEnvMonVoltageSensor Info Adapter """
    implements(ICiscoEnvMonVoltageSensorInfo)

    combined_shutdown_thresholds_string = ProxyProperty('combined_shutdown_thresholds_string')
    voltage_threshold_low = ProxyProperty('lv_threshold_string')
    voltage_threshold_high = ProxyProperty('hv_threshold_string')
    voltage_last_shutdown = ProxyProperty('voltage_last_shutdown_string')

    @property
    def status(self):
        """override the default status method to show component-specific status"""
        voltage_state = self._object.state
        if voltage_state:
            return self._object.state
        return 'Unknown'
