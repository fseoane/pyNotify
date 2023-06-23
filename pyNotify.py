
import os
import sys
import configparser
import asyncio
import threading
from gotify import AsyncGotify  
import subprocess
import json
import pystray
from PIL import Image
from psutil import Process
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from mixer import pygame

	
def checkIfFileExists(fileFullPathName):
	# Check if the file specified by fileFullPathName exists(true) or not (false).
	return os.path.isfile(fileFullPathName)

def checkIfProcessRunning(processName):
	# Check if there is any running process that contains the given name processName.
	countProcesses = 0
	for proc in psutil.process_iter():
		if (proc.name().lower() == processName.lower()):
			countProcesses+=1
   
		if (countProcesses > 2):  # each running program for pyNotify creates two processess....
			return True

	return False

def osNotify(title,message):
    subprocess.run(["notify-send", "-u", "normal", "-i", "notification", "-t", "3000",title, message],check=True)

def play_ogg(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

async def log_push_messages(tray_icon,conf_gotify_url,conf_client_token,conf_notification_sound):
	global EXIT_REQUESTED
	async_gotify = AsyncGotify(
		base_url=conf_gotify_url,
		client_token=conf_client_token,
	)
	print("...listening")
	if (tray_icon.HAS_NOTIFICATION):
		tray_icon.notify(message="...is ready and listening",title="pyNotify....")
  
	async for msg in async_gotify.stream():
		#playsound(conf_notification_sound)
		play_ogg(conf_notification_sound)
		if (tray_icon.HAS_NOTIFICATION):
			tray_icon.notify(message=msg["message"],title=msg["title"])
		else:
			#subprocess.run(["notify-send", "-u", "normal", "-i", "notification", "-t", "3000",msg["title"], msg["message"]],check=True)
			osNotify(msg["title"],msg["message"],"notification")


def tray_icon_on_clicked(tray_icon, item):
	global runner
	if str(item) == "Quit":
		tray_icon.stop()
		runner.close()
		sys.exit(0)

if __name__ == "__main__":
	global runner

	PATH_SEPARATOR = '/'
	SCRIPT_PATH = os.getcwd()
	if (SCRIPT_PATH[0]!='/'):
		PATH_SEPARATOR = '\\'
  
	# get the version of the app from file pyNotify.ver
	pyNotify_version ="??"
	with open(SCRIPT_PATH+PATH_SEPARATOR+'pyNotify.ver', 'rb') as f:
		pyNotify_version = f.read().decode('utf-8')

	progname = sys.argv[0]
	processName = progname[progname.rfind(PATH_SEPARATOR)+1:]
		
	if checkIfProcessRunning(processName):
		osNotify(
      		"pyNotify ERROR",
			"{} process already exists. {} seems to be running. Exiting".format(processName,processName)
      	)
		sys.exit(1) 

	try:   
		if (PATH_SEPARATOR == '/'):
			configFile="/etc/pyNotify.conf"
		else:
			configFile=SCRIPT_PATH+PATH_SEPARATOR+'pyNotify.conf'

		print ("Loading config from: {}".format(configFile))
		config = configparser.ConfigParser()
		if not (config.read(configFile)):
			osNotify(
					"pyNotify ERROR",
					"{} file couldn´t be found or read.".format(configFile)
				)
			sys.exit(1) 

		conf_gotify_url=config['config']['gotify_url']
		if (conf_gotify_url=="https://gotify-host:port"):
			osNotify(
					"pyNotify ERROR",
					"Configure {} with your values.".format(configFile)
				)
			sys.exit(1) 
		conf_client_token=config['config']['client_token']
  
		conf_tray_icon=SCRIPT_PATH+PATH_SEPARATOR+config['config']['tray_icon']
		if not checkIfFileExists(conf_tray_icon):
			osNotify(
				"pyNotify ERROR",
				"{} file does not exist.\nCheck your config file: {}".format(conf_tray_icon,SCRIPT_PATH+PATH_SEPARATOR+'pyNotify.conf')
			)
			sys.exit(1) 
   
		conf_notification_sound=SCRIPT_PATH+PATH_SEPARATOR+config['config']['notification_sound']
		if not checkIfFileExists(conf_notification_sound):
			osNotify(
				"pyNotify ERROR",
				"{} file does not exist.\nCheck your config file: {}".format(conf_notification_sound,SCRIPT_PATH+PATH_SEPARATOR+'pyNotify.conf')
			)
			sys.exit(1) 
	
		pyNotify_icon=PIL.Image.open(conf_tray_icon)

		tray_icon = pystray.Icon("pyNotify", pyNotify_icon, title="pyNotify", visible=True,
			menu=pystray.Menu(
				pystray.MenuItem("About",
                    pystray.Menu(
						pystray.MenuItem("     pyNotify {}".format(pyNotify_version),action=None, checked=None, radio=False, default=False, visible=True, enabled=False),
						pystray.MenuItem('    Fernando Seoane',action=None, checked=None, radio=False, default=False, visible=True, enabled=False),
						pystray.MenuItem('       Jun 2023',action=None, checked=None, radio=False, default=False, visible=True, enabled=False),
						pystray.MenuItem("───────────────────────",action=None, checked=None, radio=False, default=False, visible=True, enabled=False),
						pystray.MenuItem("Conf:  {}".format(SCRIPT_PATH+PATH_SEPARATOR+'pyNotify.conf'),action=None, checked=None, radio=False, default=False, visible=True, enabled=False),
						pystray.MenuItem("Server:{}".format(conf_gotify_url),action=None, checked=None, radio=False, default=False, visible=True, enabled=False),
						pystray.MenuItem("Token: {}".format(conf_client_token),action=None, checked=None, radio=False, default=False, visible=True, enabled=False),
    				)
                ),
				pystray.MenuItem("───────────────────────",action=None, checked=None, radio=False, default=False, visible=True, enabled=False),
				pystray.MenuItem("Quit", tray_icon_on_clicked)
			)
		)
		
		# Run the icon mainloop in first thread
		threading.Thread(target=tray_icon.run).start()
		print("...placed tray icon")

		# Run the gotify listener asynchronously in a second thread
		with asyncio.Runner() as runner:
			print("...starting loop")
			runner.run(log_push_messages(tray_icon,conf_gotify_url,conf_client_token,conf_notification_sound))
	finally:
		sys.exit(0) 