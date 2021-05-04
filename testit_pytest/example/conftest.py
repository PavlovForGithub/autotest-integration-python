import pytest
import testit


@pytest.fixture(scope='session', autouse=True)
def session_setup_teardown():
	with testit.step('session conf setup step 1'):
		with testit.step('session conf setup step 1.2'):
			assert True
	yield
	with testit.step('session conf teardown step 1'):
		with testit.step('session conf teardown step 1.2'):
			assert True


@pytest.fixture(scope='module', autouse=True)
def module_setup_teardown():
	with testit.step('module conf setup step 1'):
		with testit.step('module conf setup step 1.2'):
			assert True
	yield
	with testit.step('module conf teardown step 1'):
		with testit.step('module conf teardown step 1.2'):
			assert True


@pytest.fixture(scope='class', autouse=True)
def class_setup_teardown():
	with testit.step('class conf setup step 1'):
		with testit.step('class conf setup step 1.2'):
			assert True
	yield
	with testit.step('class conf teardown step 1'):
		with testit.step('class conf teardown step 1.2'):
			assert True


@pytest.fixture(scope='function', autouse=True)
def method_setup_teardown():
	with testit.step('method conf setup step 1'):
		with testit.step('method conf setup step 1.2'):
			assert True
	yield
	with testit.step('method conf teardown step 1'):
		with testit.step('method conf teardown step 1.2'):
			assert True
