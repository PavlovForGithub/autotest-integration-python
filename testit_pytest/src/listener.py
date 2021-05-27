import pytest
import configparser
import testit_pytest
from testit_pytest.api import Api
from testit_pytest.json_fixture import JSONFixture
from testit_pytest.utils import step
import os
from datetime import datetime
import inspect
import re


class TestITListener(object):

    def __init__(self):
        path = os.path.abspath('')
        root = path[:path.index(os.sep)]
        while not os.path.isfile(f'{path}{os.sep}connection_config.ini') and path != root:
            path = path[:path.rindex(os.sep)]
        path = f'{path}{os.sep}connection_config.ini'
        if not os.path.isfile(path):
            print('File connection_config.ini was not found!')
            raise SystemExit
        self.parser = configparser.RawConfigParser()
        self.parser.read(path)
        if not re.fullmatch(r'^(?:(?:(?:https?|ftp):)?\/\/)?(?:(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-zA-Z0-9\u00a1-\uffff][a-zA-Z0-9\u00a1-\uffff_-]{0,62})?[a-zA-Z0-9\u00a1-\uffff]\.)+(?:[a-zA-Z\u00a1-\uffff]{2,}\.?))(?::\d{2,5})?(?:[/?#]\S*)?$', self.parser.get('testit', 'url')):
            print('The wrong URL!')
            raise SystemExit
        if not re.fullmatch(r'[a-zA-Z0-9]{8}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{12}', self.parser.get('testit', 'projectID')):
            print('The wrong project ID!')
            raise SystemExit
        if not re.fullmatch(r'[a-zA-Z0-9]{8}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{12}', self.parser.get('testit', 'configurationID')):
            print('The wrong configuration ID!')
            raise SystemExit

    @pytest.hookimpl
    def pytest_sessionstart(self):
        self.requests = Api(self.parser.get('testit', 'url'), self.parser.get('testit', 'privatetoken'))
        self.testrun_id = self.requests.create_testrun(JSONFixture.create_testrun(self.parser.get('testit', 'projectID'), f'LocalRun {datetime.today().strftime("%d %b %Y %H:%M:%S")}'))
        self.requests.testrun_activity(self.testrun_id, 'start')

    @pytest.hookimpl
    def pytest_runtest_protocol(self, item):
        if hasattr(item.function, 'test_externalID'):
            if not hasattr(item.function, 'test_displayName') and not item.function.__doc__:
                self.item = None
                raise Exception(f'{item.originalname} must have @testit.displayName or documentation!')
            self.item = item
        else:
            self.item = None

    @pytest.hookimpl(hookwrapper=True)
    def pytest_fixture_setup(self, fixturedef):
        yield
        if self.item:
            steps_data, results_steps_data = step.get_steps_data()
            if fixturedef.scope != 'function':
                if not hasattr(self.item, f'test_{fixturedef.scope}_setup_steps'):
                    setattr(self.item, f'test_{fixturedef.scope}_setup_steps', [] + steps_data)
                    setattr(self.item, f'test_{fixturedef.scope}_setup_results_steps', [] + results_steps_data)
                    setattr(self.item, f'{fixturedef.scope}_setup_number', 1)
                else:
                    setattr(self.item, f'test_{fixturedef.scope}_setup_steps', getattr(self.item, f'test_{fixturedef.scope}_setup_steps') + steps_data)
                    setattr(self.item, f'test_{fixturedef.scope}_setup_results_steps', getattr(self.item, f'test_{fixturedef.scope}_setup_results_steps') + results_steps_data)
                    setattr(self.item, f'{fixturedef.scope}_setup_number', getattr(self.item, f'{fixturedef.scope}_setup_number') + 1)
            else:
                if not hasattr(self.item, 'test_method_setup_steps'):
                    self.item.test_method_setup_steps = []
                    self.item.test_method_setup_results_steps = []
                self.item.test_method_setup_steps += steps_data
                self.item.test_method_setup_results_steps += results_steps_data

    @pytest.hookimpl(hookwrapper=True, trylast=True)
    def pytest_runtest_call(self):
        yield
        if self.item:
            test_steps, test_results_steps = step.get_steps_data()
            self.item.test_steps = test_steps
            self.item.test_results_steps = test_results_steps

    @pytest.hookimpl
    def pytest_fixture_post_finalizer(self, fixturedef, request):
        if self.item:
            teardown_steps, teardown_results_steps = step.get_steps_data()
            if fixturedef.scope != 'function':
                item_id = request.session.items.index(self.item)
                while not hasattr(request.session.items[item_id], f'{fixturedef.scope}_setup_number'):
                    if not hasattr(request.session.items[item_id], f'test_{fixturedef.scope}_teardown_steps'):
                        setattr(request.session.items[item_id], f'test_{fixturedef.scope}_teardown_steps', [] + teardown_steps)
                        setattr(request.session.items[item_id], f'test_{fixturedef.scope}_teardown_results_steps', [] + teardown_results_steps)
                    else:
                        setattr(request.session.items[item_id], f'test_{fixturedef.scope}_teardown_steps', getattr(request.session.items[item_id], f'test_{fixturedef.scope}_teardown_steps') + teardown_steps)
                        setattr(request.session.items[item_id], f'test_{fixturedef.scope}_teardown_results_steps', getattr(request.session.items[item_id], f'test_{fixturedef.scope}_teardown_results_steps') + teardown_results_steps)
                    item_id -= 1
                if hasattr(request.session.items[item_id], f'{fixturedef.scope}_setup_number') and getattr(request.session.items[item_id], f'{fixturedef.scope}_setup_number') != 0:
                    if not hasattr(request.session.items[item_id], f'test_{fixturedef.scope}_teardown_steps'):
                        setattr(request.session.items[item_id], f'test_{fixturedef.scope}_teardown_steps', [] + teardown_steps)
                        setattr(request.session.items[item_id], f'test_{fixturedef.scope}_teardown_results_steps', [] + teardown_results_steps)
                    else:
                        setattr(request.session.items[item_id], f'test_{fixturedef.scope}_teardown_steps', getattr(request.session.items[item_id], f'test_{fixturedef.scope}_teardown_steps') + teardown_steps)
                        setattr(request.session.items[item_id], f'test_{fixturedef.scope}_teardown_results_steps', getattr(request.session.items[item_id], f'test_{fixturedef.scope}_teardown_results_steps') + teardown_results_steps)
                    setattr(request.session.items[item_id], f'{fixturedef.scope}_setup_number', getattr(request.session.items[item_id], f'{fixturedef.scope}_setup_number') - 1)
            else:
                if not hasattr(self.item, 'test_method_teardown_steps'):
                    self.item.test_method_teardown_steps = []
                    self.item.test_method_teardown_results_steps = []
                self.item.test_method_teardown_steps += teardown_steps
                self.item.test_method_teardown_results_steps += teardown_results_steps

    @pytest.hookimpl
    def pytest_runtest_logreport(self, report):
        if self.item:
            if report.failed:
                self.item.test_traces = report.longreprtext
            if not hasattr(self.item, 'test_duration'):
                self.item.test_duration = 0
            self.item.test_duration += report.duration * 1000

    @classmethod
    def attribute_collector(cls, item, nextitem, tree_setup_steps, tree_teardown_steps, index):
        if hasattr(item.function, 'test_externalID'):
            data = {}

            parametrize_id = []
            if item.own_markers:
                for mark in item.own_markers:
                    if mark.name == 'parametrize':
                        parametrize_id.append(item.own_markers.index(mark))

            data['externalID'] = cls.param_attribute_collector(item.function.test_externalID, item.own_markers, parametrize_id, index) if parametrize_id else item.function.test_externalID
            data['steps'] = item.test_steps if hasattr(item, 'test_steps') else []
            data['stepResults'] = item.test_results_steps if hasattr(item, 'test_results_steps') else []

            data['setUp'] = tree_setup_steps['session'] + tree_setup_steps['module'] + tree_setup_steps['class'] + tree_setup_steps['method']
            data['setUpResults'] = tree_setup_steps['session_results'] + tree_setup_steps['module_results'] + tree_setup_steps['class_results'] + tree_setup_steps['method_results']

            data['tearDown'] = tree_teardown_steps['method'] + tree_teardown_steps['class'] + tree_teardown_steps['module'] + tree_teardown_steps['session']
            data['tearDownResults'] = tree_teardown_steps['method_results'] + tree_teardown_steps['class_results'] + tree_teardown_steps['module_results'] + tree_teardown_steps['session_results']

            data['resultLinks'] = item.result_links if hasattr(item, 'result_links') else []
            data['duration'] = item.test_duration if hasattr(item, 'test_duration') else None
            data['traces'] = item.test_traces if hasattr(item, 'test_traces') else None
            data['namespace'] = item.function.__module__
            data['attachments'] = item.test_attachments if hasattr(item, 'test_attachments') else []

            i = item.function.__qualname__.find('.')
            if i != -1:
                data['classname'] = item.function.__qualname__[:i]
            else:
                data['classname'] = None

            data['links'] = []
            if hasattr(item.function, 'test_links'):
                if parametrize_id:
                    for link in item.function.test_links:
                        data['links'].append({})
                        data['links'][-1]['url'] = cls.attribute_collector_links(link, 'url', item.own_markers, parametrize_id, index)
                        if link['title']:
                            data['links'][-1]['title'] = cls.attribute_collector_links(link, 'title', item.own_markers, parametrize_id, index)
                        if link['type']:
                            data['links'][-1]['type'] = cls.attribute_collector_links(link, 'type', item.own_markers, parametrize_id, index)
                        if link['description']:
                            data['links'][-1]['description'] = cls.attribute_collector_links(link, 'description', item.own_markers, parametrize_id, index)
                else:
                    data['links'] = item.function.test_links

            data['title'] = (cls.param_attribute_collector(item.function.test_title, item.own_markers, parametrize_id, index) if parametrize_id else item.function.test_title) if hasattr(item.function, 'test_title') else None
            data['description'] = (cls.param_attribute_collector(item.function.test_description, item.own_markers, parametrize_id, index) if parametrize_id else item.function.test_description) if hasattr(item.function, 'test_description') else None

            data['labels'] = []
            if hasattr(item.function, 'test_labels'):
                if parametrize_id:
                    result, param_id = cls.mass_param_attribute_collector(item.function.test_labels[0], item.own_markers, parametrize_id, index)
                    if param_id is not None and item.function.test_labels[0][1:-1] in item.name[item.name.find('[') + 1:item.name.rfind(']')].split('-')[param_id]:
                        for label in result:
                            data['labels'].append({'name': label})
                    else:
                        data['labels'].append({'name': result})
                else:
                    for label in item.function.test_labels:
                        data['labels'].append({'name': label})

            data['workItemsID'] = []
            if hasattr(item.function, 'test_workItemsID'):
                if parametrize_id:
                    result, param_id = cls.mass_param_attribute_collector(item.function.test_workItemsID[0], item.own_markers, parametrize_id, index)
                    if param_id is not None and item.function.test_workItemsID[0][1:-1] in item.name[item.name.find('[') + 1:item.name.rfind(']')].split('-')[param_id]:
                        data['workItemsID'] = result
                    else:
                        data['workItemsID'] = [result]
                else:
                    data['workItemsID'] = item.function.test_workItemsID

            data['testResult'] = 'Failed' if hasattr(item, 'test_traces') else 'Passed'
            data['failureReasonName'] = 'TestDefect' if hasattr(item, 'test_traces') else 'NoDefect'
            data['message'] = None
            if item.own_markers:
                for mark in item.own_markers:
                    if mark.name == 'skip' or mark.name == 'skipif' and mark.args[0]:
                        data['testResult'] = 'Skipped'
                        data['failureReasonName'] = None
                        if mark.kwargs:
                            data['message'] = mark.kwargs['reason']

            if hasattr(item, 'test_message'):
                data['message'] = item.test_message

            if hasattr(item.function, 'test_displayName'):
                if parametrize_id:
                    data['autoTestName'] = cls.param_attribute_collector(item.function.test_displayName, item.own_markers, parametrize_id, index)
                else:
                    data['autoTestName'] = item.function.test_displayName
            elif item.function.__doc__:
                data['autoTestName'] = item.function.__doc__
            else:
                data['autoTestName'] = 'Test without name'
                data['testResult'] = 'Failed'
                data['failureReasonName'] = 'TestDefect'
                data['traces'] = f'>\n{inspect.getsource(item.function)}\nE {item.originalname} must have @testit.displayName or documentation!\n{item.location[0]}:{item.location[1]}: Exception'

            return data, index + 1 if nextitem and item.originalname == nextitem.originalname else 0
        return None, 0

    @staticmethod
    def param_attribute_collector(attribute, marks, parametrize_id, index):
        for ID in parametrize_id:
            if attribute[attribute.find('{') + 1:attribute.rfind('}')] in marks[ID].args[0]:
                return attribute.split('{')[0] + marks[ID].args[1][index][marks[ID].args[0].split(', ').index(attribute[attribute.find('{') + 1:attribute.rfind('}')])] + attribute.split('}')[1]
        return attribute

    @staticmethod
    def mass_param_attribute_collector(attribute, marks, parametrize_id, index):
        for ID in parametrize_id:
            if attribute[1:-1] != '' and attribute[1:-1] in marks[ID].args[0]:
                param_id = marks[ID].args[0].split(', ').index(attribute[1:-1])
                return marks[ID].args[1][index][param_id], param_id
        return attribute, None

    @staticmethod
    def attribute_collector_links(link, key, marks, parametrize_id, index):
        for ID in parametrize_id:
            if link[key][link[key].find('{') + 1:link[key].rfind('}')] in marks[ID].args[0]:
                return link[key].split('{')[0] + marks[ID].args[1][index][marks[ID].args[0].split(', ').index(link[key][link[key].find('{') + 1:link[key].rfind('}')])] + link[key].split('}')[1]
        return link[key]

    @staticmethod
    def form_tree_steps(item, tree_steps, stage):
        for scope in ('session', 'module', 'class', 'method'):
            if hasattr(item, f'test_{scope}_{stage}_steps'):
                tree_steps[scope] = getattr(item, f'test_{scope}_{stage}_steps')
                tree_steps[f'{scope}_results'] = getattr(item, f'test_{scope}_{stage}_results_steps')
            elif scope not in tree_steps:
                tree_steps[scope] = []
                tree_steps[f'{scope}_results'] = []
        return tree_steps

    @pytest.hookimpl
    def pytest_sessionfinish(self, session):
        index = 0
        tree_setup_steps = {}
        tree_teardown_steps = {}
        tests_results_data = []
        for item_id in range(len(session.items)):
            tree_setup_steps = self.form_tree_steps(session.items[item_id], tree_setup_steps, 'setup')
            tree_teardown_steps = self.form_tree_steps(session.items[item_id], tree_teardown_steps, 'teardown')
            data_item, index = self.attribute_collector(
                                    session.items[item_id],
                                    session.items[item_id + 1] if item_id + 1 < len(session.items) else None,
                                    tree_setup_steps,
                                    tree_teardown_steps,
                                    index
                                )
            if data_item:
                autotest = self.requests.get_autotest(data_item['externalID'], self.parser.get('testit', 'projectID')).json()
                if not autotest:
                    autotest_id = self.requests.create_autotest(
                        JSONFixture.create_autotest(
                            data_item['externalID'],
                            self.parser.get('testit', 'projectID'),
                            data_item['autoTestName'],
                            data_item['namespace'],
                            data_item['classname'],
                            data_item['links'],
                            data_item['steps'],
                            data_item['setUp'],
                            data_item['tearDown'],
                            data_item['title'],
                            data_item['description'],
                            data_item['labels']
                        )
                    )
                else:
                    autotest_id = autotest[0]['id']
                    if data_item['testResult'] == 'Passed':
                        self.requests.update_autotest(
                            JSONFixture.update_autotest(
                                data_item['externalID'],
                                self.parser.get('testit', 'projectID'),
                                data_item['autoTestName'],
                                data_item['namespace'],
                                data_item['classname'],
                                data_item['links'],
                                data_item['steps'],
                                data_item['setUp'],
                                data_item['tearDown'],
                                data_item['title'],
                                data_item['description'],
                                data_item['labels'],
                                autotest_id
                            )
                        )
                    else:
                        self.requests.update_autotest(
                            JSONFixture.update_autotest(
                                data_item['externalID'],
                                self.parser.get('testit', 'projectID'),
                                autotest[0]['name'],
                                autotest[0]['namespace'],
                                autotest[0]['classname'],
                                data_item['links'],
                                autotest[0]['steps'],
                                autotest[0]['setup'],
                                autotest[0]['teardown'],
                                autotest[0]['title'],
                                autotest[0]['description'],
                                autotest[0]['labels'],
                                autotest_id
                            )
                        )

                for workitem_id in data_item['workItemsID']:
                    self.requests.link_autotest(autotest_id, workitem_id)

                tests_results_data.append(
                    JSONFixture.set_results_for_testrun(
                        data_item['externalID'],
                        self.parser.get('testit', 'configurationID'),
                        data_item['testResult'],
                        data_item['stepResults'],
                        data_item['setUpResults'],
                        data_item['tearDownResults'],
                        data_item['traces'],
                        data_item['resultLinks'],
                        data_item['duration'],
                        data_item['failureReasonName'],
                        data_item['message'],
                        None,
                        data_item['attachments']
                    )
                )
        if tests_results_data:
            self.requests.set_results_for_testrun(
                self.testrun_id,
                tests_results_data
            )

    @testit_pytest.hookimpl
    def add_link(self, link_url, link_title, link_type, link_description):
        if not hasattr(self.item, 'result_links'):
            self.item.result_links = []
        self.item.result_links.append({'url': link_url, 'title': link_title, 'type': link_type, 'description': link_description})

    @testit_pytest.hookimpl
    def add_message(self, test_message):
        self.item.test_message = str(test_message)

    @testit_pytest.hookimpl
    def add_attachments(self, attach_paths):
        if not hasattr(self.item, 'test_attachments'):
            self.item.test_attachments = []
        for path in attach_paths:
            if os.path.isfile(path):
                self.item.test_attachments.append({'id': self.requests.load_attachment(open(path, "rb"))})
            else:
                print(f'File ({path}) not found!')
