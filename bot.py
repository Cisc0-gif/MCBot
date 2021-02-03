#! /usr/bin/env python3
# -*- coding:utf-8 -*-
#
# @name   : MCBotv1.0 - Java Minecraft Server Control Bot
# @url    : https://github.com/Cisc0-gif/MCBotv1.0
# @author : Cisc0-gif

import os, sys, random, time, pathlib, logging, subprocess

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

admins = []

client = discord.Client(command_prefix='/', description='Basic Commands')
TOKEN = ''

# Go To https://discordapp.com/developers/applications/ and start a new application for Token

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s'))
logger.addHandler(handler)

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

  if message.content == "/help" or message.content == "/h":
    await channel.send("/version or /v for server version\n/ulog to view bot update log\n/modlist or /mods to view server mod list\n/whoami to ping bot response\n/serverStatus to check if server is up\n/serverOn to turn server on\n/serverOff to turn server off")

  if message.content == "/version" or message.content == "/v":
    await channel.send("Running Minecraft Java Edition - v#")

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

client_run()
