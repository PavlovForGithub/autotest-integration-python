from functools import wraps
from datetime import datetime
from testit_pytest import TestITPluginManager


def inner(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        function(*args, **kwargs)
        return function
    return wrapper


def workItemID(*test_workItemsID: int or str):
    def outer(function):
        function.test_workItemsID = []
        for test_workItemID in test_workItemsID:
            function.test_workItemsID.append(str(test_workItemID))
        return inner(function)
    return outer


def displayName(test_displayName: str):
    def outer(function):
        function.test_displayName = test_displayName
        return inner(function)
    return outer


def externalID(test_externalID: str):
    def outer(function):
        function.test_externalID = test_externalID
        return inner(function)
    return outer


def title(test_title: str):
    def outer(function):
        function.test_title = test_title
        return inner(function)
    return outer


def description(test_description: str):
    def outer(function):
        function.test_description = test_description
        return inner(function)
    return outer


def labels(*test_labels: str):
    def outer(function):
        function.test_labels = test_labels
        return inner(function)
    return outer


def link(url: str, title: str = None, type: str = None, description: str = None):
    def outer(function):
        if not hasattr(function, 'test_links'):
            function.test_links = []
        function.test_links.append({'url': url, 'title': title, 'type': type, 'description': description})
        return inner(function)
    return outer


class LinkType:
    RELATED = 'Related'
    BLOCKED_BY = 'BlockedBy'
    DEFECT = 'Defect'
    ISSUE = 'Issue'
    REQUIREMENT = 'Requirement'
    REPOSITORY = 'Repository'


def addLink(url: str, title: str = None, type: str = None, description: str = None):
    if hasattr(TestITPluginManager.get_plugin_manager().hook, 'add_link'):
        TestITPluginManager.get_plugin_manager().hook.add_link(link_url=url, link_title=title, link_type=type, link_description=description)


def message(test_message: str):
    if hasattr(TestITPluginManager.get_plugin_manager().hook, 'add_message'):
        TestITPluginManager.get_plugin_manager().hook.add_message(test_message=test_message)


def attachments(*attach_paths: str):
    if hasattr(TestITPluginManager.get_plugin_manager().hook, 'add_attachments'):
        TestITPluginManager.get_plugin_manager().hook.add_attachments(attach_paths=attach_paths)


class step:
    step_stack = []
    steps_data = []
    steps_data_results = []

    def __init__(self, *args):
        self.args = args

    def __call__(self, *args, **kwargs):
        if self.args and callable(self.args[0]):
            function = self.args[0]
            dt_now = round(datetime.utcnow().timestamp() * 1000)
            name = f'Step {str(len(self.steps_data) + 1)}'
            if self.step_stack:
                for step_id in self.step_stack[1:]:
                    name += f'.{step_id + 1}'
            self.steps_data = self.step_append(
                self.steps_data,
                self.step_stack,
                name,
                function.__name__
            )
            outcome = 'Passed'
            try:
                result = function(*args, **kwargs)
            except Exception:
                outcome = 'Failed'
                raise
            finally:
                self.steps_data_results = self.result_step_append(
                    self.steps_data,
                    self.steps_data_results,
                    self.step_stack,
                    outcome,
                    round(datetime.utcnow().timestamp() * 1000) - dt_now
                )
            return result
        else:
            function = args[0]

            @wraps(function)
            def step_wrapper(*a, **kw):
                dt_now = round(datetime.utcnow().timestamp() * 1000)
                if self.args:
                    if len(self.args) == 2:
                        self.steps_data = self.step_append(
                            self.steps_data,
                            self.step_stack,
                            self.args[0],
                            self.args[1]
                        )
                    else:
                        self.steps_data = self.step_append(
                            self.steps_data,
                            self.step_stack,
                            self.args[0]
                        )
                outcome = 'Passed'
                try:
                    result = function(*a, **kw)
                except Exception:
                    outcome = 'Failed'
                    raise
                finally:
                    self.steps_data_results = self.result_step_append(
                        self.steps_data,
                        self.steps_data_results,
                        self.step_stack,
                        outcome,
                        round(datetime.utcnow().timestamp() * 1000) - dt_now
                    )
                return result
            return step_wrapper

    def __enter__(self):
        self.dt_now = round(datetime.utcnow().timestamp() * 1000)
        if len(self.args) == 2:
            self.steps_data = self.step_append(self.steps_data, self.step_stack, self.args[0], self.args[1])
        else:
            self.steps_data = self.step_append(self.steps_data, self.step_stack, self.args[0])

    def __exit__(self, exc_type, exc_value, tb):
        if not exc_type:
            outcome = 'Passed'
        else:
            outcome = 'Failed'
        self.steps_data_results = self.result_step_append(
                                    self.steps_data,
                                    self.steps_data_results,
                                    self.step_stack,
                                    outcome,
                                    round(datetime.utcnow().timestamp() * 1000) - self.dt_now
                                )

    def step_append(self, steps, step_stack, step_title, step_description=None):
        if step_stack:
            steps[step_stack[0]]['steps'] = self.step_append(steps[step_stack[0]]['steps'], step_stack[1:], step_title, step_description)
        else:
            steps.append({'title': step_title, 'description': step_description, 'steps': []})
            self.step_stack.append(len(steps) - 1)
        return steps

    def result_step_append(self, steps, steps_results, step_stack, outcome, duration):
        if len(step_stack) == 1:
            while len(steps_results) < step_stack[0] + 1:
                steps_results.append({})
            steps_results[step_stack[0]]['title'] = steps[step_stack[0]]['title']
            steps_results[step_stack[0]]['description'] = steps[step_stack[0]]['description']
            steps_results[step_stack[0]]['outcome'] = outcome
            steps_results[step_stack[0]]['duration'] = duration
            del self.step_stack[-1]
        else:
            while len(steps_results) < step_stack[0] + 1:
                steps_results.append({'stepResults': []})
            steps_results[step_stack[0]]['stepResults'] = self.result_step_append(steps[step_stack[0]]['steps'], steps_results[step_stack[0]]['stepResults'], step_stack[1:], outcome, duration)
        return steps_results

    @classmethod
    def get_steps_data(cls):
        data = cls.steps_data
        result_data = cls.steps_data_results
        cls.steps_data = []
        cls.steps_data_results = []
        return data, result_data
