===============================
ZenPacks.community.CiscoEnvMonE
===============================

About
=====

This is a heavily modified version of Egor Puzanov's original Cisco Envmon.
Thanks go to Egor for all his work..

This ZenPack is intended suppliment the hardware monitoring provided by the Zenoss
Enteprise(commercial) CiscoMonitor Zenpack.  It can be installed conflict-free
on a zenoss system alongside the existing Envmon ZenPack and or the commercial
CiscoMonitor ZenPack..

This Zenpack does not require the installation of any other ZenPack, it does not use the
Device Advaced Details ZenPack.

The Zenpack includes the following Components:
----------------------------------------------
* CiscoEnvMonFan - The Cisco Fan monitors status of fans
* CiscoEnvMonPowerSupply - The Cisco power supply monitors status of powersuppplies
* CiscoEnvMonTemperature Sensor - The Cisco temperature sensor monitors the status of temperature
  sensor health and provides high temperature thresholds based upon the actual hard-coded temperature
  shutdown threshholds built into the device.
* NEW! CiscoEnvMonVoltageSensor - The Cisco voltage sensor monitors the status of voltages sensors
  and provides high and low voltage alerts based on the actual hard-coded component voltage threshols built
  into the device.  Readings are in mv.

Zproperties to control monitoring configuration:
-----------------------------------------------
We have provides zproperties that should help you almost totally avoid having to over-ride templates locally on devices.

The list of zproperties are as follows:

* zCiscoMonTemperatureFactor (float, default: .90):   Setting this property will lower the temperature threshold by the
    the amount you specify below the device automatic shutdown threshold. For example, if a temperature sensor's shut down point
    is 40C, setting .90 will cause the zenoss thresholds to go off at 36C.
* zCiscoMonVoltageFactor (float, default: .90: Setting this property will have two effects.  First it will lower the voltage
    max threshold.  Second it will raise the voltage min threshold.  So for example if a Cisco Device will shut down
    if a voltage sensor goes below 500mv and above 1000mv, setting this property to .90 will cause a threshold alert to
    be generated if voltage drops below 450mv or above 900mv.
* zCiscoMonIgnoreNotPresent(boolean, default True): if you set this to true, any alerts showing a sensor as "notPresent" will
    have a priority of informational rather than the normal critical status.  We find in practice that
    many routers/gateways can have external 2nd power supplies that show up with a state of  notPresent when a more
    accurate state would be "not installed".
    But you can also have a situation where not present is very bad if you dont replace something or some
    component fails in a way that causes it to look "notPresent"..so we leave it up to you...
* zEnvMonMapIgnoreNames(string, default: None):  this zproperty can be used to exclude CiscoEnvMonE components from the model.  Just    add a regex, to exclude names of components from the model.  So for example to remove all componnets with the name
    that starts with CPU add ^CPU to the zproperty.  for CPU or Fan 1 do ^CPU|Fan\s1 ...

Important notes:
================

Important Note 1:  There are no mibs/traps in this ZenPack of transforms for syslogs/traps.  We tend to try to keep syslogs/traps clustered in their own separate zenpacks and not part of "polling" based zenpacks like this one..

    If you want an example on how to parse the envmon mib traps and as a bonus check to see if a component is monitored and drop the event if it isnt
        you can refer to this gist.  But as a caution...make sure you keep an eye on zeneventd.log when you add new traps because
        in the wild you can get unexpected results that break transforms.

        https://gist.github.com/dougsyer/4b21043e4e0143a20534

Important Note 2:  Unlike the CiscoEnvMon Zenpack, there is no modelling for Cisco Expansion cards built into the Zenpack.  The reason is that we use the Enterprise Zenpack to provide this modelling.

Important Note 3:  If you do decide at some point to uninstall the ORIGINAL EnvMon Zenpack, be careful because there are some version that will uninstall the entire /Cisco Event Class.

Important Note 4:  I have had limited sucess cleanly uninstalling this zenpack.  This is listed below on issues/enhancements.

Requirements
============

Zenoss
------

You must first have, or install, Zenoss 4.2.3 or later. Although we dont see any reason why
this wouldnt work on 4.1.1 and maybe 3.x. We run 4.2.3 and have no plans to test earlier
versions. You can download the free Core version of Zenoss from http://community.zenoss.org/community/download.


Installation
============

**IMPORTANT:  if you dont have this device class, you must create it before Installation:  /Network/Cisco**

Failure to do so will cause the zenpack installation to fail. This will be fixed in the next update.

Normal Installation (packaged egg)
----------------------------------

Download the XXXX
Copy this file to your Zenoss server and run the following commands as the zenoss
user.

        zenpack --install ZenPacks.community.CiscoEnvMonE-2.0.3.egg
        zenoss restart

Developer Installation (link mode)
----------------------------------

If you wish to further develop and possibly contribute back to the CiscoEnvMon
ZenPack you should clone the git `repository <https://github.com/dsyer/ZenPacks.community.CiscoEnvMonE>`_,
then install the ZenPack in developer mode using the following commands.


        git clone git://github.com/NWNCorp/ZenPacks.community.CiscoEnvMonE.git
        zenpack --link --install ZenPacks.community.CiscoEnvMonE
        zenoss restart


Usage
=====

Installing the ZenPack will add the following items to your Zenoss system.

Modeler Plugins
---------------

- **community.snmp.CiscoEnvmonFanMap** - Fan modeler plugin.
- **community.snmp.CiscoEnvMonPowerSupplyMap** - Power Supply modeler plugin.
- **community.snmp.CiscoEnvMonTemperatureSensorMap** - Temperature Sensor modeler
  plugin.
- **community.snmp.CiscoEnvMonVoltageSensorMap** - Temperature Sensor modeler
  plugin.


To use the new features, bind these templates to the device classes that house your Cisco
devices.

Monitoring Templates
--------------------
- Devices/Network/Cisco/CiscoEnvMonFan
- Devices/Network/Cisco/CiscoEnvMOnPowerSupply
- Devices/Network/Cisco/CiscoEnvMonTemperatureSensor
- Devices/Network/Cisco/CiscoEnvMonVoltageSensor

Event Classes Created
---------------------
/Events/Status/CiscoEnvMonFan
/Events/Status/CiscoEnvMonPowerSupply
/Events/Status/CiscoEnvMonTemperatureSensor
/Events/Status/CiscoEnvMonVoltageSensor

 Reports
-------

- No reports are included with this ZenPack

Updates
=================================
- Version 2.5.2
  - full z6 RM support, chagne graph sizes
  - added js renderers for status
  - various code cleanups for style a few small fixes
  - add in patch to make cisco device relations work without having to rebuild relations on new device creation
  - update graph legends for Z6
  - fix errors with voltage sensor threshold
  - fix fans being set to warning thresholds
  - add threshold event classes to go into /Threshold sub device class
  - fix voltage sensors to sho up as Voltage Sensor (envmon)
  - fix issue with temperature threshold not getting coverted to an integer.
- Version 2.2.1
  - remove dependency on impact since sometimes you need to unintall impact to upgrade it.
- Version 2.03, fixed issue where last voltage restart property
- Version 2.05
  - add logging to transforms
  - remove color codes from temperature sensors during modelling
  - fix errors with temperature sensor transforms due to incorrect access of properties
  - default temperature sensor max/mins to Maxint/2 and -Maxint-2 respectively (in case you model 0 as temperature threshold)



Future Enhancements / Known Issues
==================================
- There appears to be an issue with uninstalling where not all of the components remove.  I **may** have fixed
  this with the latest rev but havent tested removal again.  if you are going to remove this as is, id try to
  remove the components first and then uninstall it just to be safe until I test it again.
- I would love to show the current threshold values on the grid next to the shut down values but I cant
  get at the "factor" zproperties in the component to add it to the info adapter in order to add it to the
  javascript.  I can easily get to the zprops in dmd when i set my context to that component but ..
- I may at some point make the zCiscoMonIgnoreNotPresent just skip the components in model.  thats easy to do but
  personally Id rather see them there than have them hidden.  An another easy alternative is to just not bind
  any templates to these components but again, there shouldnt be alot of components per device in a not present
  state so I dont think this will cause much load but it may cause some NaN values... If i do see alot of Nan
  values i probably will not allow the templates to bind to these devices after the model.
- If you run this in parallel with the Enterprise cisco zenpack and use it to model the same components, you will have an issue where
  sometimes the events from this ZenPack will attach to the enterprise cisco zenapack components.  this shouldnt cause
  any stility issues and the worka round it to filter the components using the documentation above...if you plan to do it

Known Cisco Bugs or Quirks that can effect the ZenPack
============================================
- RPS power supplies in some routers will poll as not present but will send traps with no component in them.  this is an ios issue
  the work around it to catch and identify it in your transforms.
- In some switch models (35xx I believe) voltage sensors data is included in the temperature sensor data.  Ive made some attempt
  at identifying this condition however if you see temperature at 1000C its probably that issue
- 38XX switches will show a 0 temperature sensor threhsold.  not sure the exact ioss effected but since 38XX are fairly recent most
  or all of these as of 3/12/2015 have this issue.  The stats will probably work and some temperature sensors work but in this case
  I have disabled the temperature sensor threhsolds by setting them in the background to maxint/2 and -maxint/2-1 and made the gui
  show the sensor threshold as unknown
- some fans will model looking something like this:  Fan 1 - OK...There is no major effect other than confusion because you will
  have a component that says Fan 1 - Ok and a status of Failed or something like that and your traps may or may not match that component name
  depending on how clever you have gotten with them.  I plan on removing these in a future release.
- Some power supplies will model looking something like this:  Power Supply 1 - RPS OK.  or RPS notPresent.  Again this causes confusion.
  however due to the RPS bugs out there I have left that alone for now.
