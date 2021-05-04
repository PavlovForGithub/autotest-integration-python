import pytest
import testit_pytest
from testit_pytest.listener import TestITListener


def pytest_addoption(parser):
    parser.getgroup('testit').addoption('--testit', action='store_true', dest="testit_report", help='Pytest plugin for Test IT')


def pytest_configure(config):
    if config.option.testit_report:
        listener = TestITListener()
        config.pluginmanager.register(listener)
        testit_pytest.TestITPluginManager.get_plugin_manager().register(listener)
