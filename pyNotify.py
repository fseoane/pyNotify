
from os import path,getcwd,environ
from sys import argv, exit
import sys
import time
import json
from configparser import ConfigParser
from asyncio import Runner
import asyncio
import aiohttp
from threading import Thread
from gotify import AsyncGotify  
from subprocess import run as sp_run
from pystray import Icon, Menu, MenuItem
import socket
from PIL import Image
from psutil import process_iter
import webbrowser
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from pygame import mixer


	
def checkIfFileExists(fileFullPathName):
	# Check if the file specified by fileFullPathName exists(true) or not (false).
	return path.isfile(fileFullPathName)

def checkIfInternetIsAvailable(host="8.8.8.8", port=53, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error as ex:
        print(ex)
        return False

def checkIfProcessRunning(processName):
	# Check if there is any running process that contains the given name processName.
	countProcesses = 0
	for proc in process_iter(): 
		if (proc.name().lower() == processName.lower()):
			countProcesses+=1
   
		if (countProcesses > 2):  # each running program for pyNotify creates two processess....
			return True

	return False

def osNotify(title,message):
    sp_run(["notify-send", "-u", "normal", "-i", "notification", "-t", "3000",title, message],check=True)

def play_ogg(file_path):
    mixer.init()
    mixer.music.load(file_path)
    mixer.music.play()

async def log_gotify_push_messages(tray_icon,conf_gotify_url,conf_gotify_client_token,conf_gotify_sound):
	global on_mute
	global on_dnd 

	
	async_gotify = AsyncGotify(
		base_url=conf_gotify_url,
		client_token=conf_gotify_client_token,
	)
	
	print("...listening to Gotify at {}".format(conf_gotify_url))
	if (tray_icon.HAS_NOTIFICATION):
		tray_icon.notify(message="...is ready and listening",title="pyNotify....")

	async for msg in async_gotify.stream():
		#if (msg["title"] and msg["message"]):
		if (msg.get("title") and msg.get("message")):
			print("[!] new message at Gotify {} : {}".format(msg["title"],msg["message"]))
			if not on_mute:
				play_ogg(conf_gotify_sound)
			if not on_dnd:
				if (tray_icon.HAS_NOTIFICATION):
					tray_icon.notify(message=msg["message"],title=msg["title"])
				else:
					osNotify(msg["title"],msg["message"],"notification")

async def log_ntfy_push_messages(tray_icon,conf_ntfy_url,conf_ntfy_topics,conf_ntfy_sound):
	global on_mute
	global on_dnd 
 
	print("...listening to Ntfy at {}".format(conf_ntfy_url))
 
	async with aiohttp.request('get', "{}/{}/json".format(conf_ntfy_url,conf_ntfy_topics)) as resp:
		async for line in resp.content:
			if line:
				data = json.loads(line)
				if (data.get("event") and data.get("topic") and data.get("message")):
					if (data["event"]=="message"):
						if (data.get("title")):
							titl = "/"+data["title"]
						else:
							titl = ""
						print("[!] new message at Ntfy {}{} : {}".format(data["topic"],titl,data["message"]))
						if not on_mute:
							play_ogg(conf_ntfy_sound)
						if not on_dnd:	
							if (tray_icon.HAS_NOTIFICATION):
								tray_icon.notify(message=data["message"],title=data["topic"]+titl)
							else:
								osNotify(data["topic"]+titl,data["message"],"notification")


async def log_push_messages(have_Gotify,have_Ntfy,tray_icon,conf_gotify_url,conf_gotify_client_token,conf_gotify_sound,conf_ntfy_url,conf_ntfy_topics,conf_ntfy_sound):
	if have_Gotify and have_Ntfy:
		await asyncio.gather(
			log_gotify_push_messages(tray_icon,conf_gotify_url,conf_gotify_client_token,conf_gotify_sound),
			log_ntfy_push_messages(tray_icon,conf_ntfy_url,conf_ntfy_topics,conf_ntfy_sound),
		)
	if have_Gotify and not have_Ntfy:
		await asyncio.gather(
			log_gotify_push_messages(tray_icon,conf_gotify_url,conf_gotify_client_token,conf_gotify_sound),
		)
	if not have_Gotify and have_Ntfy:
		await asyncio.gather(
			log_ntfy_push_messages(tray_icon,conf_ntfy_url,conf_ntfy_topics,conf_ntfy_sound),
		)

def tray_icon_mute(tray_icon, item_mute):
	global on_mute
	on_mute = not item_mute.checked 


def tray_icon_dnd(tray_icon, item_dnd):
	global on_dnd
	on_dnd = not item_dnd.checked 
 
def tray_icon_gotify(tray_icon, item):
	global on_gotify_url
	webbrowser.open(on_gotify_url, new = 2)
 
def tray_icon_ntfy(tray_icon, item):
	global on_ntfy_url
	webbrowser.open(on_ntfy_url, new = 2)

def tray_icon_quit(tray_icon, item):
	global runner
	if str(item) == "Quit":
		tray_icon.stop()
		runner.close()
		exit(0)

if __name__ == "__main__":
	on_mute = False
	on_dnd = False
	have_Gotify = False
	have_Ntfy = False

	PATH_SEPARATOR = '/'
	SCRIPT_PATH = getcwd()
	if (SCRIPT_PATH[0]!='/'):
		PATH_SEPARATOR = '\\'
  	
	progname = argv[0]
	processName = progname[progname.rfind(PATH_SEPARATOR)+1:]
		
	if checkIfProcessRunning(processName):
		osNotify(
      		"pyNotify ERROR",
			"{} process already exists. {} seems to be running. Exiting".format(processName,processName)
      	)
		exit(1) 

	# get the version of the app from file pyNotify.ver
	if checkIfFileExists(SCRIPT_PATH+PATH_SEPARATOR+'pyNotify.ver'):
		with open(SCRIPT_PATH+PATH_SEPARATOR+'pyNotify.ver', 'rb') as f:
			pyNotify_version = f.read().decode('utf-8')
	else:
		pyNotify_version ="??"
	
	try:   
		configFile=""
		if (PATH_SEPARATOR == '/'):
			configFile="/etc/pyNotify.conf"
		else:
			configFile=SCRIPT_PATH+PATH_SEPARATOR+"pyNotify.conf"

		if not checkIfFileExists(configFile):
			osNotify(
				"pyNotify ERROR",
				"{} config file does not exist.".format(configFile)
			)
			print ("ERROR: Configuration file {} not found".format(configFile))
			exit(1) 
		else:
			print ("Reading config from: {}".format(configFile))
			
		config = ConfigParser()
		if not (config.read(configFile)):
			osNotify(
					"pyNotify ERROR",
					"{} file couldn´t be found or read.".format(configFile)
				)
			print ("ERROR: Could not load config from: {}".format(configFile))
			exit(1) 
		else:
			print ("...config file {} in use".format(configFile))
		
		if ('gotify' in config):
			print("...reading Gotify settings...")
			if 'gotify_url' in config['gotify']:
				conf_gotify_url=config['gotify']['gotify_url']
				if (conf_gotify_url=="https://gotify-host:port"):
					osNotify(
							"pyNotify ERROR",
							"Configure {} with your values.".format(configFile)
						)
					print ("ERROR: Configure your values at {}".format(configFile))
					exit(1) 
				else:
					on_gotify_url=conf_gotify_url
					print ("   .- Gotify URL {} ".format(conf_gotify_url))
					have_Gotify = True
			else:
				conf_gotify_url=""
				conf_gotify_client_token=""
				conf_gotify_sound=""
				have_Gotify = False


			if 'gotify_client_token' in config['gotify']:
				conf_gotify_client_token=config['gotify']['gotify_client_token']
				if ((conf_gotify_client_token=="") or (conf_gotify_client_token=="GotifyClientToken")):
					osNotify(
							"pyNotify ERROR",
							"Configure {} with your values.".format(configFile)
						)
					print ("ERROR: Configure your values at {}".format(configFile))
					exit(1) 
				else:
					print ("   .- Gotify client token {} ".format(conf_gotify_client_token))
					have_Gotify = (have_Gotify and True)
			else:
				conf_gotify_url=""
				conf_gotify_client_token=""
				conf_gotify_sound=""
				have_Gotify = False
     
			if 'gotify_sound' in config['gotify']:
				conf_gotify_sound=config['gotify']['gotify_sound']
				if (conf_gotify_sound==""):
					osNotify(
							"pyNotify ERROR",
							"Configure {} with your values.".format(configFile)
						)
					print ("ERROR: Configure your values at {}".format(configFile))
					exit(1) 
				else:
					print ("   .- Gotify sound {} ".format(conf_gotify_sound))
		else:
			conf_gotify_url=""
			conf_gotify_client_token=""
			conf_gotify_sound=""
			have_Gotify = False

		if ('ntfy' in config):
			print("...reading Ntfy settings...")
			if 'ntfy_url' in config['ntfy']:
				conf_ntfy_url=config['ntfy']['ntfy_url']
				if (conf_ntfy_url=="https://ntfy-host:port"):
					osNotify(
							"pyNotify ERROR",
							"Configure {} with your values.".format(configFile)
						)
					print ("ERROR: Configure your values at {}".format(configFile))
					exit(1) 
				else:
					on_ntfy_url=conf_ntfy_url
					print ("   .- Ntfy URL {} ".format(conf_ntfy_url))
					have_Ntfy = True
			else:
				conf_ntfy_url=""
				conf_ntfy_topics=""
				conf_ntfy_sound=""
				have_Ntfy = False
			
			if 'ntfy_topics' in config['ntfy']:
				conf_ntfy_topics=config['ntfy']['ntfy_topics']
				if (conf_ntfy_topics==""):
					osNotify(
							"pyNotify ERROR",
							"Configure {} with your values.".format(configFile)
						)
					print ("ERROR: Configure your values at {}".format(configFile))
					exit(1) 
				else:
					print ("   .- Ntfy topics {} ".format(conf_ntfy_topics))
					have_Ntfy = (have_Ntfy and True)
			else:
				conf_ntfy_url=""
				conf_ntfy_topics=""
				conf_ntfy_sound=""
				have_Ntfy = False

			if 'ntfy_sound' in config['ntfy']:
				conf_ntfy_sound=config['ntfy']['ntfy_sound']
				if (conf_ntfy_sound==""):
					osNotify(
							"pyNotify ERROR",
							"Configure {} with your values.".format(configFile)
						)
					print ("ERROR: Configure your values at {}".format(configFile))
					exit(1) 
				else:
					print ("   .- Ntfy sound {} ".format(conf_ntfy_sound))
		else:
			conf_ntfy_url=""
			conf_ntfy_topics=""
			conf_ntfy_sound=""
			have_Ntfy = False
		
		if 'config' in config:
			if 'tray_icon' in config['config']:
				conf_tray_icon=SCRIPT_PATH+PATH_SEPARATOR+config['config']['tray_icon']
				if not checkIfFileExists(conf_tray_icon):
					osNotify(
						"pyNotify ERROR",
						"{} file does not exist. Check your config file: {}".format(conf_tray_icon,SCRIPT_PATH+PATH_SEPARATOR+'pyNotify.conf')
					)
					print ("ERROR: Tray icon file {} not found".format(conf_tray_icon))
					exit(1) 
				else:
					print ("   .- App tray icon {} ".format(conf_tray_icon))
		
				pyNotify_icon=Image.open(conf_tray_icon) 
				print("...built tray icon image")
			else:
				pyNotify_icon=Image.open(SCRIPT_PATH+PATH_SEPARATOR+"notificatoin.png") 
		else:
			pyNotify_icon=Image.open(SCRIPT_PATH+PATH_SEPARATOR+"notificatoin.png") 


		tray_icon = Icon("pyNotify", pyNotify_icon, title="pyNotify", visible=True,
			menu=Menu(
				MenuItem("Silent mode (no sound)", tray_icon_mute, checked=lambda item_mute: on_mute),
				MenuItem("Do not disturb", tray_icon_dnd, checked=lambda item_dnd: on_dnd),
				MenuItem("───────────────────────",action=None, checked=None, radio=False, default=False, visible=True, enabled=False),
				MenuItem("Open Gotify", tray_icon_gotify),
				MenuItem("───────────────────────",action=None, checked=None, radio=False, default=False, visible=True, enabled=False),
				MenuItem("Open Ntfy", tray_icon_ntfy),
    			MenuItem("───────────────────────",action=None, checked=None, radio=False, default=False, visible=True, enabled=False),
				MenuItem("About",
					Menu(
						MenuItem(" pyNotify {}".format(pyNotify_version),action=None, checked=None, radio=False, default=False, visible=True, enabled=False),
						MenuItem(' Fernando Seoane',action=None, checked=None, radio=False, default=False, visible=True, enabled=False),
						MenuItem(' -Jun 2023-',action=None, checked=None, radio=False, default=False, visible=True, enabled=False),
						MenuItem("───────────────────────",action=None, checked=None, radio=False, default=False, visible=True, enabled=False),
						MenuItem(" Config:        {}".format(configFile),action=None, checked=None, radio=False, default=False, visible=True, enabled=False),
						MenuItem(" Gotify Server: {}".format(conf_gotify_url),action=None, checked=None, radio=False, default=False, visible=True, enabled=False),
						MenuItem(" Gotify Token:  {}".format(conf_gotify_client_token),action=None, checked=None, radio=False, default=False, visible=True, enabled=False),
						MenuItem(" Ntfy Server:   {}".format(conf_ntfy_url),action=None, checked=None, radio=False, default=False, visible=True, enabled=False),
						MenuItem(" Ntfy Topics:   {}".format(conf_ntfy_topics),action=None, checked=None, radio=False, default=False, visible=True, enabled=False),
					)
				),
				MenuItem("───────────────────────",action=None, checked=None, radio=False, default=False, visible=True, enabled=False),
				MenuItem("Quit", tray_icon_quit)
			)
		)
		print("...built tray menu")


  
  		# Run the icon mainloop in first thread
		Thread(target=tray_icon.run).start()
		print("...placed icon in tray")

		# Delay 3 minutes to ensure network is ready
		print("...delayed start to ensure network is ready")
		isAvailable=False
		counter=0
		sys.stdout.write("[%s]" % (" " * 12))
		sys.stdout.flush()
		sys.stdout.write("\b" * (12+1)) # return to start of line, after '['
		while ((not isAvailable) and (counter < 36)):
			time.sleep(5)
			counter += 1
			isAvailable=checkIfInternetIsAvailable()
			sys.stdout.write("-")
			sys.stdout.flush()
		sys.stdout.write("]\n")

		# Run the listeners asynchronously in a second thread
		with Runner() as runner:
			print("...starting loop")
			runner.run(log_push_messages(have_Gotify,have_Ntfy,tray_icon,conf_gotify_url,conf_gotify_client_token,conf_gotify_sound,conf_ntfy_url,conf_ntfy_topics,conf_ntfy_sound))

   
	except Exception as error:
		# handle the exception
		print("An exception occurred:", error)
	
	finally:
		exit(0) 