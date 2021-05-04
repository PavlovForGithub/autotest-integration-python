import pytest
import testit
from os.path import join, dirname


def setup_module():
	with testit.step('Unittest test_case_1 setup module step 1'):
		assert True


def teardown_module():
	with testit.step('Unittest test_case_1 teardown module step 1'):
		assert True


class Test1:
	def setup_class(self):
		with testit.step('Test1 unittest test_case_1 class step 1'):
			assert True

	def setup_method(self):
		with testit.step('Test1 unittest test_case_1 method step 1'):
			assert True

	def teardown_class(self):
		with testit.step('Test1 unittest test_case_1 class step 1'):
			with testit.step('Test1 unittest test_case_1 class step 1.1'):
				with testit.step('Test1 unittest test_case_1 class step 1.1.1'):
					assert True

	def teardown_method(self):
		with testit.step('Test1 unittest test_case_1 method step 1'):
			with testit.step('Test1 unittest test_case_1 method step 1.1'):
				with testit.step('Test1 unittest test_case_1 method step 1.1.1'):
					assert True

	@testit.workItemID(627)
	@testit.displayName('Simple autotest 1 - {name}')
	@testit.externalID('Simple_autotest1_{name}')
	@testit.title('Authorization')
	@testit.description('E2E_autotest')
	@testit.labels('{labels}')
	@testit.link(url='https://roviti2348.atlassian.net/browse/JCP-15593')
	@testit.link(url='{url}', type='{link_type}', title='{link_title}')
	@pytest.mark.parametrize('name, labels, url, link_type, link_title', [
		('param 1',	['E2E', 'test'],	'https://dumps.example.com/module/JCP-15593',		testit.LinkType.DEFECT,			'JCP-15593'),
		('param 2',	(),					'https://github.com/testit-tms/listener-csharp',	testit.LinkType.RELATED,		'Listener'),
		('param 3',	('E2E', 'test'),	'https://best-tms.testit.software/projects',		testit.LinkType.REQUIREMENT,	''),
		('param 4',	{'E2E', 'test'},	'https://testit.software/',							testit.LinkType.BLOCKED_BY,		'Test IT'),
		('param 5',	'test',				'https://github.com/testit-tms',					testit.LinkType.REPOSITORY,		'GitHub')
	])
	def test_1(self, name, labels, url, link_type, link_title):
		testit.addLink(title='component_dump.dmp', type=testit.LinkType.RELATED, url='https://dumps.example.com/module/some_module_dump')
		testit.addLink(title='component_dump.dmp', type=testit.LinkType.BLOCKED_BY, url='https://dumps.example.com/module/some_module_dump')
		testit.addLink(title='component_dump.dmp', type=testit.LinkType.DEFECT, url='https://dumps.example.com/module/some_module_dump')
		testit.addLink(title='component_dump.dmp', type=testit.LinkType.ISSUE, url='https://dumps.example.com/module/some_module_dump')
		testit.addLink(title='component_dump.dmp', type=testit.LinkType.REQUIREMENT, url='https://dumps.example.com/module/some_module_dump')
		testit.addLink(title='component_dump.dmp', type=testit.LinkType.REPOSITORY, url='https://dumps.example.com/module/some_module_dump')
		with testit.step('Log in the system', 'system authentication'):
			with testit.step('Enter the login', 'login was entered'):
				with testit.step('Enter the password', 'password was entered'):
					assert True
			with testit.step('Create a project', 'the project was created'):
				with testit.step('Enter the project', 'the contents of the project are displayed'):
					assert True
				with testit.step('Create a test case', 'test case was created'):
					assert True
		with testit.step('Attachments'):
			testit.attachments(join(dirname(__file__), 'docs/text_file.txt'), join(dirname(__file__), 'pictures/picture.jpg'), join(dirname(__file__), 'docs/document.docx'))
			testit.attachments(join(dirname(__file__), 'docs/document.doc'), join(dirname(__file__), 'docs/logs.log'))
			assert True
		with testit.step('step 3'):
			assert True
		with testit.step('step 4'):
			assert True


@testit.externalID('Simple_test_skip')
@testit.displayName('Simple test skip')
@pytest.mark.skipif(True, reason='Because i can')
def test_skip():
	assert True


class Test22:
	def setup_class(self):
		with testit.step('Test22 unittest test_case_1 class step 1'):
			assert True

	def setup_method(self):
		with testit.step('Test22 unittest test_case_1 method step 1'):
			assert True

	def teardown_class(self):
		with testit.step('Test22 unittest test_case_1 class step 1'):
			with testit.step('Test22 unittest test_case_1 class step 1.1'):
				with testit.step('Test22 unittest test_case_1 class step 1.1.1'):
					assert True

	def teardown_method(self):
		with testit.step('Test22 unittest test_case_1 method step 1'):
			with testit.step('Test22 unittest test_case_1 method step 1.1'):
				with testit.step('Test22 unittest test_case_1 method step 1.1.1'):
					assert True

	@testit.externalID('Simple_autotest2')
	def test_2(self):
		"""Simple autotest 2"""
		assert one_step()
		assert two_step()


@testit.step
def one_step():
	assert one_one_step()
	assert one_two_step()
	return True


@testit.step
def two_step():
	testit.attachments(join(dirname(__file__), 'pictures/picture.jpg'), join(dirname(__file__), 'docs/document.docx'))
	return True


@testit.step('step 1.1', 'description')
def one_one_step():
	return True


@testit.step('step 1.2')
def one_two_step():
	return True
