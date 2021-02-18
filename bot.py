#! /usr/bin/env python3
# -*- coding:utf-8 -*-
#
# @name   : MCBotv1.1 - Java Minecraft Server Control Bot
# @url    : https://github.com/Cisc0-gif/MCBot
# @author : Cisc0-gif

import os, sys, random, time, pathlib, logging, subprocess, json, sqlite3

reqs = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'])
installed_packages = [r.decode().split('==')[0] for r in reqs.split()]
if 'discord' not in installed_packages:
  print("Package 'discord' not installed, installing now...")
  subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'discord'])

reqs = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'])
installed_packages = [r.decode().split('==')[0] for r in reqs.split()]
if 'asyncio' not in installed_packages:
  print("Package 'asyncio' not installed, installing now...")
  subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'asyncio'])

reqs = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'])
installed_packages = [r.decode().split('==')[0] for r in reqs.split()]
if 'pathlib' not in installed_packages:
  print("Package 'pathlib' not installed, installing now...")
  subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pathlib'])

import discord, asyncio, pathlib

client = discord.Client(command_prefix='/', description='Basic Commands')
TOKEN = ''

# Go To https://discordapp.com/developers/applications/ and start a new application for Token

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s'))
logger.addHandler(handler)

def convert(old):   #for converting list of tuples into list of strings
  new = []
  for i in range(0, len(old)):
    new.append(old[i][0])
  return new

def client_run():
  client.loop.create_task(background_loop())
  client.run(TOKEN)

def logwrite(msg): #writes chatlog to MESSAGES.log
  with open('MESSAGES.log', 'a+') as f:
    f.write(msg + '\n')
  f.close()

async def background_loop():
  await client.wait_until_ready()
  while not client.is_closed:
    print("Booted Up @ " + time.ctime())
    logwrite("Booted Up @ " + time.ctime())
    await asyncio.sleep(3600)  #Bootup Message

@client.event
async def on_ready():
  print('--------------------------------------------------------------------------------------')
  print('Server Connect Link:')
  print('https://discordapp.com/api/oauth2/authorize?scope=bot&client_id=' + str(client.user.id))
  print('--------------------------------------------------------------------------------------')
  print('Logged in as:')
  print(client.user.name)
  print("or")
  print(client.user)
  print("UID:")
  print(client.user.id)
  print('---------------------------------------------------')
  print('Running Minecraft Java Edition - v#')
  print('---------------------------------------------------')
  print("LIVE CHAT LOG - See MESSAGES.log For History")
  print("---------------------------------------------------")
  await client.change_presence(activity=discord.Game("MC v#"), status=discord.Status.online)

@client.event
async def on_member_join(member):
  print("Member:", member, "joined!")
  logwrite("Member: " + str(member) + " joined!")

@client.event
async def on_member_remove(member):
  print("Member:", member, "removed!")
  logwrite("Member: " + str(member) + " removed!")

@client.event
async def on_guild_role_create(role):
  print("Role:", role, "was created!")
  logwrite("Role: " + str(role) + " was created!")

@client.event
async def on_guild_role_delete(role):
  print("Role:", role, "was deleted!")
  logwrite("Role: " + str(role) + " was deleted!")

@client.event
async def on_guild_channel_create(channel):
  print("Channel:", channel, "was created!")
  logwrite("Channel: " + str(channel) + " was created!")

@client.event
async def on_guild_channel_delete(channel):
  print("Channel:", channel, "was deleted!")
  logwrite("Channel: " + str(channel) + " was deleted!")

@client.event
async def on_guild_channel_update(before, after):
  print("Channel Updated:", after)
  logwrite("Channel Updated: " + str(after))

@client.event
async def on_message(message):
  channel = message.channel
  
  if message.author == client.user:
    return #ignore what bot says in server so no message loop
  print(message.author, "said:", message.content, "-- Time:", time.ctime()) #reports to discord.log and live chat
  logwrite(str(message.author) + " said: " + str(message.content) + "-- Time: " + time.ctime())
  
  file = pathlib.Path("Members.db")
  if file.exists():
    pass
  else:
    print("Database 'Members.db' doesn't exist! Creating 'Members.db' now...")
    conn = sqlite3.connect("Members.db")
    crsr = conn.cursor()
    crsr.execute("CREATE TABLE users ( perms INTEGER, name VARCHAR(20) );")
    conn.commit()
    conn.close()
    
  conn = sqlite3.connect("Members.db") #open connection to users.db
  crsr = conn.cursor()
  crsr.execute("SELECT name FROM users")
  names0 = crsr.fetchall()
  names = convert(names0) #converted list of tuples into strings
  crsr.execute("SELECT name FROM users WHERE perms == '0'")
  users0 = crsr.fetchall()
  users = convert(users0) 
  crsr.execute("SELECT name FROM users WHERE perms == '1'")
  admins0 = crsr.fetchall()
  admins = convert(admins0)

  if str(message.author) not in names:
    crsr.execute("INSERT INTO users VALUES (?, ?)", (0, str(message.author)))
    conn.commit()

  if message.content == "/help" or message.content == "/h":
    await channel.send("/version or /v for server version\n/ulog to view bot update log\n/modlist or /mods to view server mod list\n/whoami to ping bot response\n/serverStatus to check if server is up\n/serverOn* to turn server on\n/serverOff* to turn server off\n/ops lists users with operator permission\n/motd sets the message of the day\n/users displays list of low-level users in discord server\n/admins displays admin-level users in discord server\n/addAdmin* promotes user to admin-level access")

  if message.content == "/version" or message.content == "/v":
    await channel.send("Running Minecraft Java Edition - v#")

  if message.content == "/users":
    await channel.send("Low-priv Users: ")
    for i in range(0, len(users)):
      await channel.send("- " + str(users[i]))

  if message.content == "/admins":
    await channel.send("Admin Users: ")
    for i in range(0, len(admins)):
      await channel.send("- " + str(admins[i]))

  if message.content == "/addAdmin":
    if str(message.author) in admins:
      await channel.send("Type /user USERNAME#1234")
      def check(msg):
        return msg.content.startswith('/user')
      message = await client.wait_for('message', check=check)
      user = message.content[len('/user'):].strip()
      if user not in names:
        await channel.send("User '" + user + "' not in database, adding as admin now...")
        crsr.execute("INSERT INTO users VALUES (?, ?)", (1, user))
        conn.commit()
      elif user in admins:
        await channel.send("User '" + user + "' already has Admin")
      else:
        crsr.execute("UPDATE users SET perms == '1' WHERE name == '" + user + "'")
        conn.commit()
        await channel.send("User '" + user + "' was made an Admin, Congratulations!")
    else:
      await channel.send("Acces Denied...")

  if message.content == "/serverStatus":
    file = pathlib.Path("server.lock")
    if file.exists():
      await channel.send(":Server: *On*")
    else:
      await channel.send(":Server: *Off* - Use /serverOn to start it")

  if message.content == "/serverOn":
    file = pathlib.Path("server.lock")
    if file.exists():
      await channel.send(":Server: already running...")
    elif str(message.author) in admins:
      await channel.send("Type /pass PASSWORDHERE")
      def check(msg):
        return msg.content.startswith('/pass')
      message = await client.wait_for('message', check=check)
      pword = message.content[len('/pass'):].strip()
      if pword == "PASSWORD":
        await channel.send("Starting server, please wait 1 minute for server to initialize...")
        os.system("start cmd.exe /c java -Xms####M -Xmx####M -jar SERVER.jar && echo >> server.lock")
      else:
        await channel.send("https://static.wikia.nocookie.net/jurassicpark/images/b/b3/Ahahahreal.gif/revision/latest/scale-to-width-down/340?cb=20170722184515")
    else:
      await channel.send("Access Denied...")

  if message.content == "/serverOff":
    file = pathlib.Path("server.lock")
    if file.exists() == False:
      await channel.send(":Server: already off...")
    elif str(message.author) in admins:
      await channel.send("Type /pass PASSWORDHERE")
      def check(msg):
        return msg.content.startswith('/pass')
      message = await client.wait_for('message', check=check)
      pword = message.content[len('/pass'):].strip()
      if pword == "PASSWORD":
        await channel.send("Stopping server...")
        os.system("taskkill /IM java.exe /F")
        os.system("del server.lock")
      else:
        await channel.send("https://static.wikia.nocookie.net/jurassicpark/images/b/b3/Ahahahreal.gif/revision/latest/scale-to-width-down/340?cb=20170722184515")
    else:
      await channel.send("Access Denied...")

  if message.content == "/ulog": #if author types /ulog bot displays updatelog
    try:
      f = open("update_log.txt","r+")
      if f.mode == "r+":
        contents = f.read()
        await channel.send(contents)
    finally:
      f.close()

  if message.content == "/motd":
    await channel.send("Type /message MESSAGE")
    def check(msg):
      return msg.content.startswith('/message')
    message = await client.wait_for('message', check=check)
    motd = message.content[len('/message'):].strip()
    with open("server.properties", "r") as f:
      contents = f.read().splitlines()
      contents[27] = "motd=" + str(motd)
    f.close()
    with open("server.properties", "w") as w:
      w.write("\n".join(contents))
    w.close()
    await channel.send("MOTD set to: " + str(motd))
      
  if message.content == "/mods" or message.content == "/modlist":
    try:
      f = open("modList.txt","r+")
      if f.mode == 'r+':
        contents = f.read()
        parsed = contents.splitlines()
        for i in parsed:
          await channel.send(i)
    finally:
      f.close()
      
  if message.content == "/ops":
    try:
      with open("ops.json", "r") as f:
        data = json.load(f)
      await channel.send(":Operators:")
      for i in range(0, len(data)):
        await channel.send(" -" + str(data[i]["name"]))
    finally:
      f.close()

  if message.content == "/whoami": #if author types /whoami bot responds with username
    await channel.send(message.author)

  if message.content == "/nickname": #if author types /nickname bot asks for input for new nickname
    await channel.send("Type /name nicknamehere")
    def check(msg):
        return msg.content.startswith('/name')
    message = await client.wait_for('message', check=check)
    name = message.content[len('/name'):].strip()
    await channel.send('{} is your new nickname'.format(name))
    await message.author.edit(nick=name)

  if message.content == "/dm": #if author types /dm bot creates dm with author
    await channel.send("Creating DM with " + str(message.author))
    await message.author.send('*DM started with ' + str(message.author) + '*')
    await message.author.send('Hello!')

  conn.close() #close users.db connection

client_run()
