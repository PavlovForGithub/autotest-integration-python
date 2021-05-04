class JSONFixture:

	@staticmethod
	def create_autotest(
			external_id,
			project_id,
			name,
			namespace,
			classname,
			links,
			steps,
			setup,
			teardown,
			title,
			description,
			labels
		):
		json = {
			'externalId': external_id,
			'projectId': project_id,
			'name': name,
			'namespace': namespace,
			'classname': classname,
			'links': links,
			'steps': steps,
			'setup': setup,
			'teardown': teardown,
			'title': title,
			'description': description,
			'labels': labels
		}
		return json

	@staticmethod
	def update_autotest(
			external_id,
			project_id,
			name,
			namespace,
			classname,
			links,
			steps,
			setup,
			teardown,
			title,
			description,
			labels,
			ID
		):
		json = {
			'externalId': external_id,
			'projectId': project_id,
			'name': name,
			'namespace': namespace,
			'classname': classname,
			'links': links,
			'steps': steps,
			'setup': setup,
			'teardown': teardown,
			'title': title,
			'description': description,
			'labels': labels,
			'id': ID
		}
		return json

	@staticmethod
	def create_testrun(project_id, name):
		json = {
			'projectId': project_id,
			'name': name
		}
		return json

	@staticmethod
	def set_results_for_testrun(
			autotest_external_id,
			configuration_id,
			outcome,
			step_results,
			setup_results,
			teardown_results,
			traces,
			links,
			duration,
			failure_reason_name,
			message,
			parameters
		):
		json = {
			'configurationId': configuration_id,
			'links': links,
			'autoTestExternalId': autotest_external_id,
			'outcome': outcome,
			'traces': traces,
			'stepResults': step_results,
			'setupResults': setup_results,
			'teardownResults': teardown_results,
			'duration': duration,
			'failureReasonName': failure_reason_name,
			'message': message,
			'parameters': parameters
		}
		return json
