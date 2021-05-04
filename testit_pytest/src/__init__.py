from testit_pytest.plugin_manager import TestITPluginManager
from pluggy import HookimplMarker

hookimpl = HookimplMarker("testit")

__all__ = [
    'TestITPluginManager',
    'hookimpl'
]
