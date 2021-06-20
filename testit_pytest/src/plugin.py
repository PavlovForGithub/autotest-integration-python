import testit_pytest
from testit_pytest.listener import TestITListener


def pytest_addoption(parser):
    parser.getgroup('testit').addoption(
        '--testit',
        action='store_true',
        dest="testit_report",
        help='Pytest plugin for Test IT'
    )
    parser.getgroup('testit').addoption(
        '--testrunid',
        action="store",
        dest="set_testrun",
        metavar="5236eb3f-7c05-46f9-a609-dc0278896464",
        help='Set Test-run ID'
    )
    parser.getgroup('testit').addoption(
        '--testit_url',
        action="store",
        dest="set_url",
        metavar="https://demo.testit.software",
        help='Set location of the Test IT instance'
    )
    parser.getgroup('testit').addoption(
        '--privatetoken',
        action="store",
        dest="set_privatetoken",
        metavar="T2lKd2pLZGI4WHRhaVZUejNl",
        help='Set API secret key'
    )
    parser.getgroup('debug').addoption(
        '--testit_proxy',
        action="store",
        dest="set_testit_proxy",
        metavar='{"http": "http://localhost:8888", "https": "http://localhost:8888"}',
        help='Set proxy for sending requests'
    )


def pytest_configure(config):
    if config.option.testit_report:
        listener = TestITListener(config.option.set_testrun,
                                  config.option.set_url,
                                  config.option.set_privatetoken,
                                  config.option.set_testit_proxy)
        config.pluginmanager.register(listener)
        testit_pytest.TestITPluginManager.get_plugin_manager().register(listener)
