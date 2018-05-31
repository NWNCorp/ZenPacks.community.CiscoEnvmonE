""" patches to Zenoss Model DeviceHW places these relations under device.hw.(relation)"""

from Products.ZenModel.DeviceHW import DeviceHW
from Products.ZenRelations.RelSchema import ToManyCont, ToOne

DeviceHW._relations += (("ciscoenvvoltagesensors", ToManyCont(
    ToOne, "ZenPacks.community.CiscoEnvMonE.CiscoEnvMonVoltageSensor", "hw")), )
DeviceHW._relations += (("ciscoenvtempsensors", ToManyCont(
    ToOne, "ZenPacks.community.CiscoEnvMonE.CiscoEnvMonTemperatureSensor", "hw")), )
DeviceHW._relations += (("ciscoenvfans", ToManyCont(
    ToOne, "ZenPacks.community.CiscoEnvMonE.CiscoEnvMonFan", "hw")), )
DeviceHW._relations += (("ciscoenvpowersupplies", ToManyCont(
    ToOne, "ZenPacks.community.CiscoEnvMonE.CiscoEnvMonPowerSupply", "hw")), )
