"""
patches for Cisco Monitor.
The Cisco Monitor zenpack (probably inadvertantly) messes up inherited relations from Device and other os/hw things.

even relatinos directly appliked to the ciscoDevice class have issues on instanitation of devices not getting relations.
but subclasses of CiscoDevice are fine at least they are for me.

i have a couple theories on why this is but basically the way they do the relations in CiscoDevice makes those
relations more static than other classes, in part to protect relations overlap but I think its probably a mistake
that they have yet to fix and i havent felt like chasing them about it.  even the default calcperf relation
doesnt take on the Cisco Device (at all even on buildRelations AFIK...)

again i know why and there are ways to add relations to Cisco Device and have it inherit from Device.Device..
I have dont it n other ZenPacks and it doesnt involve hacking the CiscoDevice.py file...but anyways since we are
only overriding hwdevice relations we can just make sure that we load up CiscoDevice here fist and this
SHould fix the issue with Cisco devices not getting this relations without doing a buildRelations..

"""
# pylint: disable=F0002, W0603, W0621, E0602

from Products.ZenUtils.Utils import monkeypatch

DeviceHW = None

@monkeypatch('ZenPacks.zenoss.CiscoMonitor.CiscoDevice.CiscoDevice')
def __init__(self, *args, **kwargs):
    """ see warnings above """

    global DeviceHW

    if DeviceHW is None:
        from Products.ZenModel.DeviceHW import DeviceHW

    original(self, *args, **kwargs)
