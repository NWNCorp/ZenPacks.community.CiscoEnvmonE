""" patches to Zenoss Model DeviceHW places these relations under device.hw.(relation)"""

# pylint: disable=F0002, W0603, W0621

DeviceHW = None

def patchHWRelations():
    """ use lazy import to patch device HW """

    from Products.ZenRelations.RelSchema import ToManyCont, ToOne
    global DeviceHW

    if DeviceHW is None:
        from Products.ZenModel.DeviceHW import DeviceHW

    DeviceHW._relations += (("ciscoenvvoltagesensors", ToManyCont(
        ToOne, "ZenPacks.community.CiscoEnvMonE.CiscoEnvMonVoltageSensor", "hw")), )
    DeviceHW._relations += (("ciscoenvtempsensors", ToManyCont(
        ToOne, "ZenPacks.community.CiscoEnvMonE.CiscoEnvMonTemperatureSensor", "hw")), )
    DeviceHW._relations += (("ciscoenvfans", ToManyCont(
        ToOne, "ZenPacks.community.CiscoEnvMonE.CiscoEnvMonFan", "hw")), )
    DeviceHW._relations += (("ciscoenvpowersupplies", ToManyCont(
        ToOne, "ZenPacks.community.CiscoEnvMonE.CiscoEnvMonPowerSupply", "hw")), )
