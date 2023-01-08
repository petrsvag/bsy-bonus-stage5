import requests
import json

class GithubGist:
	def __init__(self, token: str, name: str, debug_info = False):
		self.token = token
		self.name = name
		self.header = {'Authorization': 'token {}'.format(self.token)}
		self.params = {'scope': 'gist'}
		self.API_URL = 'https://api.github.com/gists'
		self.API_URL_WITH_ID = None
		self.DESCRIPTION = 'This gist was created for stage 5 of bonus assignment. ({})'.format(name)
		self.debug_info = debug_info
		self.activity_file = "activity-{}.json".format(self.name)
		self.questions_file = 'questions-{}'.format(self.name)
		self.get_or_create_gist()

	def delete(self):
		response = self.send_request(method='DELETE')
		if response.status_code != 204:
			self.debug('Error while deleting gist: ', response.text)

	def debug(self, *values):
		if self.debug_info:
			print(*values)

	def send_request(self, method, url=None , params = None, data = None, header = {}):
		for k, v in self.header.items():
			if k not in header.keys():
				header[k] = v
		header = header or self.header
		url = url or self.API_URL_WITH_ID or self.API_URL

		data = json.dumps(data)
		return requests.request(method=method,url=url,headers=header,data=data, params=params)

	def get_or_create_gist(self):
		self.id = self.find_gist().get('id')
		if not self.id:
			self.create_gist()
		self.API_URL_WITH_ID = self.API_URL + '/' + self.id

	def get_gist(self):
		response = self.send_request(method='GET')
		if response.status_code != 200:
			self.debug('Unable to get list of gists. Response code: ', response.status_code, response.text)
			return {}

		return response.json()

	def find_gist(self):
		response = self.send_request(method='GET',url=self.API_URL)
		if response.status_code != 200:
			self.debug('Unable to get list of gists. Response code: ', response.status_code, response.text)
			return {}
		for gist in response.json():
			if gist['description'] == self.DESCRIPTION:
				return gist
		return {}

	def get_file(self, filename) -> dict:
		gist = self.get_gist()
		if 'files' not in gist.keys():
			return None
		return self.get_gist()['files'][filename]

	def update_file(self, filename, content):
		data = {'files' : {filename: {'content': content}}}
		response = self.send_request('PATCH', data=data)
		if response.status_code == 200:
			return response.json()
		return None

	def create_gist(self):
		parameters = {'scope': 'gist'}
		data = {"description": self.DESCRIPTION,
				   "public": False,
				   "files": {self.activity_file: {"content": "{}"}, self.questions_file: {"content": "Hello all i have few questions to ask: \n"}}}
		response = self.send_request(url=self.API_URL ,method='POST', params=parameters, data=data)
		if response.status_code != 201:
			raise Exception("Error while creating gist", response.text)
		self.update_gist(response.json())

	def update_gist(self, gist):
		self.id = gist['id']
		self.API_URL_WITH_ID = self.API_URL + "/" + self.id

	def get_comments(self) -> list:
		response = self.send_request(method='GET', url=self.API_URL_WITH_ID + '/comments')
		if response.status_code == 200:
			return response.json()
		self.debug('Error while getting comments:', response.text)
		return None


	def create_comment(self, message) -> dict:
		response = self.send_request(url=self.API_URL_WITH_ID + '/comments', method='POST', data={'body' :message})
		if response.status_code == 201:
			return response.json()
		self.debug('Error while creating comment:', response.text)
		return None
