import pytest
import testit


def setup_module():
	with testit.step('unittest setup test_2 module step 1'):
		assert True


def teardown_module():
	with testit.step('unittest teardown test_2 module step 1'):
		assert True


@testit.workItemID('{wi}')
@testit.displayName("Тест 6 - ({value_type})")
@testit.externalID("{value_id}")
@testit.link(url='{url}', title='This is {title_link}')
@testit.labels('{labels}')
@testit.title('{title}')
@pytest.mark.parametrize('wi, value_type, value_id, labels, title, url, title_link', [
	(627,			"FLOAT",	'ext_float',	('area', 'test'),	'name1',	'https://dumps.example.com/module/some_module_dump',	''),
	((627, 766),	"LONG",		'ext_long',		'area',				'name2',	'https://vk.com',										''),
	([767, 627],	"STRING",	'ext_string',	('Area12', 'teg'),	'name3',	'https://ok.ru',										'ok.ru'),
	(766,			"BOOL",		'ext_bool',		[],					'name4',	'https://google.com',									'GOOGLE'),
	('766',			"DOUBLE",	'ext_double',	'23',				'name5',	'https://youtube.com',									'Русская локализация')
])
def test_6(wi, value_type, value_id, labels, title, url, title_link):
	testit.addLink(title='component_dump.dmp', type=testit.LinkType.RELATED, url='https://dumps.example.com/module/some_module_dump')
	testit.addLink(type=testit.LinkType.BLOCKED_BY, url='https://dumps.example.com/module/some_module_dump')
	testit.addLink(type=testit.LinkType.DEFECT, url='https://dumps.example.com/module/some_module_dump')
	testit.addLink(type=testit.LinkType.ISSUE, url='https://dumps.example.com/module/some_module_dump')
	testit.addLink(type=testit.LinkType.REQUIREMENT, url='https://dumps.example.com/module/some_module_dump')
	testit.addLink(type=testit.LinkType.REPOSITORY, url='https://demo.testit.software/projects/4/autotests/test-runs/e267a03b-fa03-41ba-9812-c803c828237f')
	with testit.step('step 1'):
		with testit.step('step 1.1'):
			with testit.step('step 1.1.1'):
				assert True
		with testit.step('step 1.2'):
			with testit.step('step 1.2.1'):
				assert True
			with testit.step('step 1.2.2'):
				assert True
	with testit.step('step 2'):
		assert True
	with testit.step('step 3'):
		assert True
	with testit.step('step 4'):
		assert True


class Test34:
	@testit.displayName('displayName8')
	@testit.externalID('externalID8')
	def test_8(self):
		assert True

	@testit.externalID('Номер теста 7')
	@pytest.mark.skipif(True, reason='Because i can')
	def test_7(self):
		"""Test 7"""
		assert True
