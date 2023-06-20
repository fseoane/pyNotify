
import os
import sys
import configparser
import asyncio
import threading
from gotify import AsyncGotify    # pip install gotify
import subprocess
import json
from playsound import playsound
import pystray
import PIL.Image
import psutil
 
def checkIfProcessRunning(processName):
	'''
	Check if there is any running process that contains the given name processName.
	'''
	#Iterate over the all the running process
	countProcesses = 0
	for proc in psutil.process_iter():
		if (proc.name().lower() == processName.lower()):
			countProcesses+=1
   
		if (countProcesses > 2):  # each running program for pyNotify creates two processess....
			return True

	return False


async def log_push_messages(conf_gotify_url,conf_client_token,conf_notification_sound,conf_notification_icon):
	global EXIT_REQUESTED
	async_gotify = AsyncGotify(
		base_url=conf_gotify_url,
		client_token=conf_client_token,
	)
	print("...listening")
	async for msg in async_gotify.stream():
		playsound(conf_notification_sound)
		subprocess.run(["notify-send", "-u", "normal", "-i", conf_notification_icon, "-t", "3000",msg["title"], msg["message"]],check=True)


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
  
	progname = sys.argv[0]
	processName = progname[progname.rfind(PATH_SEPARATOR)+1:]
	print ("Checking if {} is already running...".format(processName))
		
	if checkIfProcessRunning(processName):
		print ("{} process already exists. {} seems to be running. Exiting".format(processName,processName))
		sys.exit(1) 

	try:   
		print ("Loading config from: {}".format(SCRIPT_PATH+PATH_SEPARATOR+'pyNotify.conf'))
		config = configparser.ConfigParser()
		config.read(SCRIPT_PATH+PATH_SEPARATOR+'pyNotify.conf')

		conf_gotify_url=config['config']['gotify_url']
		conf_client_token=config['config']['client_token']
		conf_tray_icon=SCRIPT_PATH+PATH_SEPARATOR+config['config']['tray_icon']
		conf_notification_sound=SCRIPT_PATH+PATH_SEPARATOR+config['config']['notification_sound']
		conf_notification_icon=config['config']['notification_icon_name']

		print("Creating tray icon: {}".format(conf_tray_icon))
		pyNotify_icon=PIL.Image.open(conf_tray_icon)

		tray_icon = pystray.Icon("pyNotify", pyNotify_icon, title="pyNotify", visible=True,
			menu=pystray.Menu(
				pystray.MenuItem("Quit", tray_icon_on_clicked)
			)
		)
		
		# Run the icon mainloop in a separate thread
		threading.Thread(target=tray_icon.run).start()
  
		# Run the gotify listener second thread
		print ("...connecting to : {} as client: {}".format(conf_gotify_url,conf_client_token))
		with asyncio.Runner() as runner:
			runner.run(log_push_messages(conf_gotify_url,conf_client_token,conf_notification_sound,conf_notification_icon))
		#asyncio.run(log_push_messages(conf_gotify_url,conf_client_token,conf_notification_sound,conf_notification_icon))
	finally:
		print("Finishing...")