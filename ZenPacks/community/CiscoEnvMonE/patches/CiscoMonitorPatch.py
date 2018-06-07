"""
patches for Cisco Monitor.
The Cisco Monitor zenpack tries to exclude relations inherited from Products.ZenModel.Device and
OperatingSystem/DeviceHW.  it does this by explicitly setting only some relations to inherit in CiscoDevice.CiscoDevice
and then calling Device.__init__ and ManagedEnttity.__init__ in a super command.

We dont want to completely remove this protection and we dont want to manually patch the file, so we came up with
this work around which forces the module to load with the patches settings

You wouldnt need this if you could guarantee that this zenpack would be loaded earlier in the easy_install.pth
and you dont need to do this for sub-classes of cisco device.

Even without this patch if you do a buildRelations on the device after it picks up its python class it would get the
new relation.

There may be a more elegant way of doing this, i know there are more fragile ways and more complicated ways but this
seems fairly innocent and it is working for other zenpacks and should be fairly future proof.

In this zenpack since we are only updating hwrelations this is pretty safe and shouldnt override the protections on
the zenpack for device level relations although it could in theory cause an issue with globally overriden base
hw classes or inherited hw classes applied globally but I think this is a fairly safe thing.

we could also jsut have this a device level relation but i really like having my clear hw components under device.hw and
os under device .os.

if you had device level relations for cisco device you can follow a similar pattern or you could

Again use caution if you are using this as a template for overriding classes...in production if you break or
worse change existing relations you can pretty much destroy your zodb sometimes that is temporary ie you just break
relations
but if you instantiate then change relations you can be in big trouble since all the wrappers around the zodb/aquisition/
property code in zenoss makes it really hard to hack things out of the zodb using std zodb t-shooting..

I warned you if you copy this ....be careful know what you are doing and test especially if you are migrationg to differnt
relationship names with existing objects that have those relations instantiated...

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
