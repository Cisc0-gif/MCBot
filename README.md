# MCBotv1.0 - Discord bot to control your Java Minecraft Servers (Windows Only)

**UPDATE:** Added new /ops and /motd commands

A simple bot compatible with all Minecraft Java servers (modded or not) to post mod links, control the server, and a few other discord commands.

## Features
* Permission and password protected commands
* Mod list for Modded server communities
* Several useful discord cmdline tools
* Discord chat log

## Getting Started

### Get your Discord Application Token
Go to the [Discord Developer Portal](<https://discordapp.com/developers/applications/>) and click 'New Application'. Go through the setup and go to the 'Bot' tab on the left. From there click 'Copy' under 'Token' and paste it into the var TOKEN in bot.py.

### Vanilla - Get your Minecraft Server
Go to the [Minecraft Java Edition: Server download page](<https://www.minecraft.net/en-us/download/server/>) and click the download link. Save it in an empty folder.

### Forge - Get your Modded Minecraft Server
Go to the [Forge Server download page](<http://files.minecraftforge.net/maven/net/minecraftforge/forge/index_1.16.4.html>) and download the latest installer. Next, run the installer, select the 'Install server' option, and changed the directory on the bottom to any empty directory, then continue the installation. Once done, run the ``` forge-....jar ``` file, edit the ``` eula.txt ``` file and set ``` eula=true ```. 

### Transfer over MCBotv1.0 files into your Server directory
Next, move modList.txt, bot.py, and update_log.txt into your server directory. Edit modList to include the links of your mods for your server's community and edit update_log.txt with changes if you'd like to.

### Configue MCBotv1.0
Lastly, we'll add admins to your bot, set a password, and configure your server.jar file. Open 'bot.py' in any editor and in the var "admins", enter the names of discord users you wish to be able to turn the server on or off (Ex. Name#1234). Now go down to the ``` /serverOn ``` and ``` /serverOff ``` commands and in the lines ``` if pword == "PASSWORD" ``` and change PASSWORD to whatever you want. Next go to ``` os.system('start cmd.exe... ``` and change the ``` server.jar ``` portion to the name of your server jar file. That's it! Now just run the bot with ``` python3 bot.py ``` and in discord, turn the server on with ``` /serverOn ```.

## Built With

* Python3.7 - Easy to learn programming language!
* Java - Main language of Minecraft
* Discord.py - Python library for creating Discord bots
* Kali Linux - Pentesting OS developed by Offensive Security
* GitHub - This Website!

## Authors

* **Cisc0-gif** - *Main Contributor/Author*: Ecorp7@protonmail.com

## License

This project is licensed under the GNU General Public License v3 - see the LICENSE file for details

## Acknowledgments

All credits are given to the authors and contributors to tools used in this software
