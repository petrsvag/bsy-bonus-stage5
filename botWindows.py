from bot import Bot
import subprocess


class BotWindows(Bot):
	def get_all_users(self):
		ret = subprocess.check_output('net user', shell=True)
		return ret.decode('windows-1252')

	def list_directory_content(self, path):
		return subprocess.check_output(['powershell','dir', path]).decode('windows-1252')

	def get_system_info_detailed(self):
		return subprocess.check_output(['powershell', 'systeminfo /fo csv | ConvertFrom-Csv | select OS*, System*, Hotfix* | Format-List']).decode('windows-1252')

	def get_all_logged_in_users(self):
		return subprocess.check_output(['powershell', 'query user /server:$SERVER']).decode('windows-1252')

	def execute_binary(self, binary, arguments):
		return subprocess.check_output([binary, arguments]).decode('windows-1252')
