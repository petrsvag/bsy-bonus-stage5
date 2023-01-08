# BSY - stage 5
Small application using github gist to comunicate between main unit(master.py) and bots (bot.py)

Droids and main unit have two mandatory parameters:
- ```GITHUB_API_TOKEN``` - Github token to access Github Gists
- ```GIST_NAME``` - selected namepsace to connect master unit to bots

## Commands
The main unit supports 11 commands (commands cen by selected using numbers 1-10 and 2l):
 - 1 - Show how many droids are in the namepsace and how many are online (last active previous heartbeat)
 - 2 - List all users in system
 - 2l - Show only logged in users
 - 3 - Get information about the bot user
 - 4 - List content of specified directory with permissions
 - 5 - List content of specified directory only with item names
 - 6 - Copy file from bot to the master(controller)
 - 7 - Execute binary on the bots (you have to specify path to binary and arguments)
 - 8 - Get information about the system os
 - 9 - Get detailed information about the system os
 - 10 - Quit

 All commands are in ```variables.py``` in ```COMMANDS``` variable.

## Comunication
Master is the one that creates and deletes the gist used for comunication.
### Heartbeat
The bots write to file that is named ```activity-{namepsace}.json``` their last active time the master reads the file and based on how many keys there are determines how many bots totaly were at some point in the namespace online bots are detected by the time it takes between heartbeats if the time is smaller they are online.

### Tasks
The master uses file ```questions-{namespace}``` to write english sentanced based on which the bots respond with comment eather with sentence or by sending an image that has secret message inside it (this is determined by the definition of the commands in ```variables.py``` in ```COMMANDS``` variable).

## Screenshots
![master and two bots](screenshots/Sn%C3%ADmek%20obrazovky%202023-01-08%20124026.png)
![gist](screenshots/Sn%C3%ADmek%20obrazovky%202023-01-08%20124733.png)