from bot import Bot
import os
import pwd, grp
import subprocess

class BotLinux(Bot):

	def get_all_users(self):
		res = []
		for p in pwd.getpwall():
			res.append(p[0] + " " + grp.getgrgid(p[3])[0])
		return "\n".join(res)

	def get_bots_user(self):
		return os.environ['LOGNAME']

	def list_directory_content(self,path):
		return subprocess.check_output('ls -la {}'.format(path), shell=True).decode()

	def get_system_info_detailed(self):
		return subprocess.check_output('uname -a', shell=True).decode()

	def get_all_logged_in_users(self):
		return subprocess.check_output('who', shell=True).decode()

	def execute_binary(self, binary, arguments):
		return subprocess.check_output([binary, arguments]).decode()