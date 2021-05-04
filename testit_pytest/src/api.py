import requests
import os
import mimetypes


class Api(object):

	def __init__(self, url, private_token):
		self.url = url
		self.headers = {'Authorization': 'PrivateToken ' + private_token}
		mimetypes.add_type('text/plain', '.log')

	# AutoTests
	def create_autotest(self, json):
		response = requests.post(self.url + '/api/v2/autoTests', headers=self.headers, json=json)
		print(f"Autotest: {json['name']}")
		if response.status_code == 201:
			print('\nCreate autotest passed!')
			return response.json()['id']
		else:
			print(f"Create autotest error: {response.json()['error']['key']}")

	def link_autotest(self, autotest_id, workitem_id):
		response = requests.post(f'{self.url}/api/v2/autoTests/{autotest_id}/workItems', headers=self.headers, json={'id': workitem_id})
		if response.status_code == 204:
			print('Link autoTest with workItems passed!')
		else:
			print(f"Link autoTest with workItems error: {response.json()['error']['key']}")

	def get_autotest(self, external_id, project_id):
		response = requests.get(f'{self.url}/api/v2/autoTests?projectId={project_id}&externalId={external_id}', headers=self.headers)
		if response.status_code == 200:
			print('\nGet autoTest passed!')
			return response
		else:
			print(f"Get autoTest error: {response.json()['error']['key']}")

	def update_autotest(self, json):
		response = requests.put(self.url + '/api/v2/autoTests', headers=self.headers, json=json)
		print(f"AutoTest: {json['name']}")
		if response.status_code == 204:
			print('Update passed!')
		else:
			print(f"Update error: {response.json()['error']['key']}")

	# TestRuns
	def create_testrun(self, json):
		response = requests.post(self.url + '/api/v2/testRuns', headers=self.headers, json=json)
		if response.status_code == 201:
			print('Create testRun passed!')
			return response.json()['id']
		else:
			print(f"Create testRun error: {response.json()['error']['key']}")

	def set_results_for_testrun(self, testrun_id, json):
		response = requests.post(f'{self.url}/api/v2/testRuns/{testrun_id}/testResults', headers=self.headers, json=json)
		if response.status_code == 200:
			print('Set results passed!')
			return response.json()
		else:
			print(f"Set results error: {response.json()['error']['key']}")

	def testrun_activity(self, testrun_id, action):
		response = requests.post(f'{self.url}/api/v2/testRuns/{testrun_id}/{action}', headers=self.headers)
		if response.status_code == 204:
			print(f'TestRun {action} passed!')
		else:
			print(f"TestRun {action} error: {response.json()['error']['key']}")

	def link_attachment(self, test_result_id, file):
		response = requests.post(f'{self.url}/api/v2/testResults/{test_result_id}/attachments', headers=self.headers, files={'file': (os.path.basename(file.name), file, mimetypes.guess_type(file.name)[0])})
		if response.status_code == 200:
			print('Link attachment passed!')
		else:
			print(f"Link attachment error: {response.json()['error']['key']}")
