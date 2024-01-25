
from os import path,getcwd,environ
from sys import argv, exit
import time
import requests
import json
from configparser import ConfigParser
from asyncio import Runner
from threading import Thread
from gotify import AsyncGotify  
#from ntfpy import NTFYClient
#from ntfpy import NTFYUser
from subprocess import run as sp_run
from pystray import Icon, Menu, MenuItem
from PIL import Image
from psutil import process_iter
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from pygame import mixer
import webbrowser

	
def checkIfFileExists(fileFullPathName):
	# Check if the file specified by fileFullPathName exists(true) or not (false).
	return path.isfile(fileFullPathName)

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


async def log_gotify_push_messages(tray_icon,conf_gotify_url,conf_client_token,conf_notification_sound):
	global on_mute
	global on_dnd 
	
	async_gotify = AsyncGotify(
		base_url=conf_gotify_url,
		client_token=conf_client_token,
	)
	
	## Ref: https://ntfpy.nevdocs.xyz/
 	#import ntfpy
 	#import asyncio
	#async def main():
	#	ntfyClient = ntfpy.NTFYClient(ntfpy.NTFYServer("https://ntfy.sh"), "test", ntfpy.NTFYUser("user", "pass"))
	#	await ntfyClient.subscribe(tray_icon.notify(message,title))
	#if __name__ == "__main__":
 	# 	asyncio.run(main())
 
	print("...listening at {}".format(conf_gotify_url))
	if (tray_icon.HAS_NOTIFICATION):
		tray_icon.notify(message="...is ready and listening",title="pyNotify....")

	async for msg in async_gotify.stream():
		if not on_mute:
			play_ogg(conf_notification_sound)
		if not on_dnd:
			if (tray_icon.HAS_NOTIFICATION):
				tray_icon.notify(message=msg["message"],title=msg["title"])
			else:
				osNotify(msg["title"],msg["message"],"notification")

async def log_ntfy_push_messages(tray_icon,conf_ntfy_url,conf_ntfy_topics,conf_notification_sound):
	global on_mute
	global on_dnd 
 
	print("...listening at {}".format(conf_ntfy_url))
	resp = requests.get("{}/{}/json".format(conf_ntfy_url,conf_ntfy_topics), stream=True)
	for line in resp.iter_lines():
		if line:
			data = json.loads(line)
			if (data["event"]=="message"):
				if not on_mute:
					play_ogg(conf_notification_sound)
				if not on_dnd:
					if (tray_icon.HAS_NOTIFICATION):
						tray_icon.notify(message=data["message"],title=data["topic"]+"/"+data["title"])
					else:
						osNotify(data["title"],data["topic"]+"/"+data["message"],"notification")


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

		conf_client_token=config['gotify']['client_token']
		print ("   .- Gotify client token {} ".format(conf_client_token))

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
		
		conf_ntfy_topics=config['ntfy']['ntfy_topics']
		print ("   .- Ntfy topics {} ".format(conf_ntfy_topics))
		
		conf_tray_icon=SCRIPT_PATH+PATH_SEPARATOR+config['config']['tray_icon']
		if not checkIfFileExists(conf_tray_icon):
			osNotify(
				"pyNotify ERROR",
				"{} file does not exist. Check your config file: {}".format(conf_tray_icon,SCRIPT_PATH+PATH_SEPARATOR+'pyNotify.conf')
			)
			print ("ERROR: Tray icon file {} not found".format(conf_tray_icon))
			exit(1) 
		else:
			print ("   .- Icon {} ".format(conf_tray_icon))
		
		conf_notification_sound=SCRIPT_PATH+PATH_SEPARATOR+config['config']['notification_sound']
		if not checkIfFileExists(conf_notification_sound):
			osNotify(
				"pyNotify ERROR",
				"{} file does not exist.\nCheck your config file: {}".format(conf_notification_sound,SCRIPT_PATH+PATH_SEPARATOR+'pyNotify.conf')
			)
			print ("ERROR: Notification sound file {} not found".format(conf_notification_sound))
			exit(1) 
		else:
			print ("   .- Notif {} ".format(conf_notification_sound))
		
		pyNotify_icon=Image.open(conf_tray_icon) 
		print("...built tray icon image")


		tray_icon = Icon("pyNotify", pyNotify_icon, title="pyNotify", visible=True,
			menu=Menu(
				MenuItem("Silent mode (no sound)", tray_icon_mute, checked=lambda item_mute: on_mute),
				MenuItem("Do not disturb", tray_icon_dnd, checked=lambda item_dnd: on_dnd),
				MenuItem("───────────────────────",action=None, checked=None, radio=False, default=False, visible=True, enabled=False),
				MenuItem("Open Gotify", tray_icon_gotify),
				MenuItem("───────────────────────",action=None, checked=None, radio=False, default=False, visible=True, enabled=False),
				MenuItem("Open Ntfy", tray_icon_gotify),
    			MenuItem("───────────────────────",action=None, checked=None, radio=False, default=False, visible=True, enabled=False),
				MenuItem("About",
					Menu(
						MenuItem(" pyNotify {}".format(pyNotify_version),action=None, checked=None, radio=False, default=False, visible=True, enabled=False),
						MenuItem(' Fernando Seoane',action=None, checked=None, radio=False, default=False, visible=True, enabled=False),
						MenuItem(' -Jun 2023-',action=None, checked=None, radio=False, default=False, visible=True, enabled=False),
						MenuItem("───────────────────────",action=None, checked=None, radio=False, default=False, visible=True, enabled=False),
						MenuItem(" Config:        {}".format(configFile),action=None, checked=None, radio=False, default=False, visible=True, enabled=False),
						MenuItem(" Gotify Server: {}".format(conf_gotify_url),action=None, checked=None, radio=False, default=False, visible=True, enabled=False),
						MenuItem(" Gotify Token:  {}".format(conf_client_token),action=None, checked=None, radio=False, default=False, visible=True, enabled=False),
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
		print("...delayed start (3 minutes) to ensure network is ready")
		time.sleep(180)

		# Run the gotify listener asynchronously in a second thread
		with Runner() as runner:
			print("...starting loop")
			runner.run(log_gotify_push_messages(tray_icon,conf_gotify_url,conf_client_token,conf_notification_sound))
			#runner.run(log_ntfy_push_messages(tray_icon,conf_ntfy_url,conf_ntfy_topics,conf_notification_sound))

	except Exception as error:
		# handle the exception
		print("An exception occurred:", error)
	
	finally:
		exit(0) 