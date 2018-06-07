""" patch loader for zenpack
    optional_import is zenoss copyrighted code
"""

import logging
from importlib import import_module
from ZenPacks.community.CiscoEnvMonE.patches import DeviceHWPatches

LOG = logging.getLogger('zen.CiscoEnvMonE')

def optional_import(module_name, patch_module_name):
    """Import patch_module_name only if module_name is importable."""
    try:
        import_module(module_name)
    except ImportError:
        pass
    else:
        try:
            import_module(
                '.{0}'.format(patch_module_name),
                'ZenPacks.community.CiscoEnvMonE.patches')
        except ImportError:
            LOG.exception("failed to apply %s patches", patch_module_name)

DeviceHWPatches.patchHWRelations()

optional_import('ZenPacks.zenoss.CiscoMonitor', 'CiscoMonitorPatch')



