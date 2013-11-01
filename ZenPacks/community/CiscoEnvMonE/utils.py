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

# adding these here because there are transforms that use these codes also
from re import search


def decode_envmon_state(code):
    """ returns State text for cisco envmon mib CiscoEnvMonState """
    return {0: 'Unknown',
            1: 'Normal',
            2: 'Warning',
            3: 'Critical',
            4: 'Shutdown',
            5: 'notPresent',
            6: 'notFunctioning'}.get(int(code), 'Unknown')


def decode_ps_source(code):
    """ returns State text for cisco envmon mib ciscoEnvMonSupplySource  """
    return {1: 'Unknown',
            2: 'ac',
            3: 'dc',
            4: 'externalPowerSupply',
            5: 'internalRedundant'}.get(int(code), 'Unknown')


def match_exclude_regex(dev, comp_name, map_type, log):
    dontCollectNames = getattr(dev, 'zEnvMonMapIgnoreNames', None)
    if dontCollectNames and search(dontCollectNames, comp_name):
        log.info( "CiscoEnvMonComponent %s name %s matched the"
            "zEnvMonMapIgnoreNames zprop '%s, excluing from model'" % (comp_name, map_type, dontCollectNames))
        return True
    return False
