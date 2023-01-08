#!/usr/bin/python3 -u
import json, sys, os, time, datetime, piScreenUtils

skriptPath = os.path.dirname(os.path.abspath(__file__))
os.chdir(skriptPath)


def printHelp():
	print("This tool is desigend for syscalls.\nSo you have one script, which controlls everything and get every info about.")
	print("""
-h or --help
	Show this information
-v
	Shows detailed informations during execution
--start-browser <URL>
	Starts the Browser
--stop-browser
	Stops the Browser when active
--restart-browser
	Restart the Browser when active
--start-vlc <file>
	Starts VLC Player
--stop-vlc
	Stops VLC Player when active
--restart-vlc
	Restarts the VLC Player when active
--pause-vlc
	Pause/Play the video if mode ist VLC
--play-vlc
	Play the video if mode is VLC
--start-impress <file>
	Starts Libreoffice Impress
--stop-impress
	Stops Libreoffice Impress when active
--restart-impress
	Restarts Libreoffice Impress when active
--reboot
	Restarts the Device
--shutdown
	Shutdown the Device
--configure-desktop [<--mode> <mode>] [<--wallpaper> <path>] [<--color> <hexColor>]
	Configure the desktop wallpaper.
	Possible modes are: color|stretch|fit|crop|center|tile|screen
	Hex colors has 6 characters and starts with a hash. Keep in mind, this character has to be escaped with a backslash!
--get-desktop-configuration
	Returns the full desktop configuration
--get-status
	Returns a JSON String with statusinfos
--screen-on
	Turns the screen on
--screen-standby
	Turns the screen in standby
--screen-off
	Turns the screen off
--screen-switch-input
	Tells the display to change the input to our system,
	if it is not currently displayed
--get-website
	Get the current in settings configured website
--get-mode
	Get the current mode [firefox|vlc|impress|none]
--set-pw <user> [-f <file with password>] [password]
	Change the password for the weblogin user. Removes the old password.
	You can set the password directly --change-pw <user> <password>
	or you can set the password by file --change-pw <user> -f <file>
	File will be erased after command!
	Special characters in password are only in file mode available!
--check-update [--draft] [--pre-release]
	Check for updates on Github
	If you are using --draft or --pre-release parameter, then you check this channels too
--do-upgrade [--draft] [--pre-release]
	Check for updates, download install files if release is available and do upgrade.
	Sudo rights are requiered!
--set-display-protocol <protocol>
	Set the display protocol to CEC, DDC or MANUALLY.
--get-display-protocol
	Retuns the current activ display protocol. CEC or DDC
--set-display-orientation [--no-save] <orientation ID>
	0 = 0 degrees
	1 = 90 degrees
	2 = 180 degrees
	3 = 270 degrees
	If --no-save is set, the orientation will be not permanent.
--get-display-orientation-settings
	Returns the display orientation in settingsfile.
--get-display-orientation
	Returns the display orientation from os.
--schedule-firstrun
	Start schedule firstrun manually.
--schedule-lastcron
	Start last crontab entry
--schedule-manually-command <--commandID> <commandID> [<--parameter> <parameter>]
	Runs a single command selected by commandid
--schedule-manually-commandset <--id> <index>
	Runs the commandset selected by id in schedule
--schedule-manually-cron <--index> <index>
	Runs the cron entry selected by index in schedule
--schedule-manually-trigger <--index> <index>
	Runs the trigger selected by index in schedule
--add-cron <--pattern <pattern>> [--enabled <false/true>] [--commandset <commandsetID>] [--start <"JJJJ-MM-DD hh:mm">] [--end <"JJJJ-MM-DD hh:mm">] [--command <commandID>] [--parameter <parameter>]
	Add a cronentry to schedule.json.
--update-cron <--index <cronIndex>> [--enabled [false/true]] [--commandset [commandsetID]] [--start ["JJJJ-MM-DD hh:mm"]] [--end ["JJJJ-MM-DD hh:mm"]] [--command [commandID]] [--parameter [parameter]] [--pattern <pattern>]
	Update a cronentry by index in schedule.json.
--delete-cron <--index <cronIndex>>
	Delete a cronentry by index from schedule.json.
--add-trigger <--trigger <triggerID>> [--enabled <true/false>] [--command:<caseName> <commandID>] [--parameter:<caseName> <parameter>] [--commandset:<caseName> <commandsetID>]
	Add a trigger to schedule.json.
	If the trigger needs additional parameters, so you can add them like this: [--<parameterName> <parameterValue>]
--update-trigger <--index <triggerIndex>> [--trigger <triggerID>] [--enabled <true/false>] [--command:<caseName> <commandID>] [--parameter:<caseName> <parameter>] [--commandset:<caseName> <commandsetID>]
	Update a trigger by index in schedule.json.
	If the trigger needs additional parameters, so you can add them like this: [--<parameterName> <parameterValue>]
--delete-trigger <--index <triggerIndex>>
	Delete a trigger by index from schedule.json.
--add-commandset <--name <name>> [--command <commandID> [parameter]]
	Add a commandset to schedule.json.
--update-commandset <--id <id>> [--name <name>] [--command <commandID> [parameter]]
	Update a commandset by id in schedule.json.
--delete-commandset <--id <id>>
	Delete a commandset by id from schedule.json.
	""")

def checkForRootPrivileges():
	if os.geteuid() != 0:
		verbose and print("Please run this function with root privileges.")
		return False
	return True

def loadSettings():
	return json.load(open(piScreenUtils.paths.settings))

def loadSchedule():
	return json.load(open(piScreenUtils.paths.schedule))

def loadManifest():
	return json.load(open(piScreenUtils.paths.manifest))

def endAllModes():
	piScreenUtils.logging.debug("End all modes")
	try:
		if os.path.exists(piScreenUtils.paths.modeFirefox):
			os.remove(piScreenUtils.paths.modeFirefox)
			os.system("killall -q -SIGTERM firefox-esr")
		if os.path.exists(piScreenUtils.paths.modeVLC):
			os.remove(piScreenUtils.paths.modeVLC)
			os.system("killall -q -SIGTERM vlc")
		if os.path.exists(piScreenUtils.paths.modeImpress):
			os.remove(piScreenUtils.paths.modeImpress)
			os.system("killall -q -SIGTERM soffice.bin")
	except:
		piScreenUtils.logging.error("Unable to end mode")
	

def startBrowser(parameter):
	piScreenUtils.logging.info("Start browser")
	endAllModes()
	f = open(piScreenUtils.paths.modeFirefox,"w")
	f.write(parameter)
	f.close()

def stopBrowser():
	piScreenUtils.logging.info("Stop browser")
	endAllModes()

def restartBrowser():
	piScreenUtils.logging.info("Restart browser")
	os.system("killall -q -SIGTERM firefox-esr")

def startVLC(parameter,soft=False):
	piScreenUtils.logging.info("Start VLC")
	if not soft:
		endAllModes()
	f = open(piScreenUtils.paths.modeVLC,"w")
	f.write(parameter)
	f.close()

def stopVLC():
	piScreenUtils.logging.info("Stop VLC")
	endAllModes()

def restartVLC():
	piScreenUtils.logging.info("Restart VLC")
	os.system("killall -q -SIGTERM vlc")

def startImpress(parameter):
	piScreenUtils.logging.info("Start impress")
	endAllModes()
	f = open(piScreenUtils.paths.modeImpress,"w")
	f.write(parameter)
	f.close()

def stopImpress():
	piScreenUtils.logging.info("Stop impress")
	endAllModes()

def restartImpress():
	piScreenUtils.logging.info("Restart impress")
	os.system("killall -q -SIGTERM soffice.bin")

def reboot():
	piScreenUtils.logging.info("Reboot system")
	verbose and print("Reboot system")
	os.system("reboot")

def shutdown():
	piScreenUtils.logging.info("Shutdown system")
	verbose and print("Shutdown system")
	os.system("poweroff")

def configureDesktop():
	piScreenUtils.logging.debug("Configure desktop")
	try:
		os.environ["DISPLAY"] = ":0"
		os.environ["XAUTHORITY"] = "{userHomePath}.Xauthority"
		os.environ["XDG_RUNTIME_DIR"] = "/run/user/1000"
		if f"--mode" in sys.argv:
			indexOfElement = sys.argv.index(f"--mode") + 1
			if indexOfElement >= len(sys.argv) or sys.argv[indexOfElement].startswith("--"):
				piScreenUtils.logging.warning("No parameter given")
				verbose and print("No parameter given")
			else:
				if sys.argv[indexOfElement].lower() in ["color", "stretch", "fit", "crop", "center", "tile", "screen"]:
					piScreenUtils.logging.info(f"Set wallpaper mode to {os.path.abspath(sys.argv[indexOfElement])}")
					os.system(f"pcmanfm --wallpaper-mode={sys.argv[indexOfElement].lower()}")
				else:
					piScreenUtils.logging.warning("No possible mode selected")
					verbose and print("No possible mode selected")
		if f"--wallpaper" in sys.argv:
			indexOfElement = sys.argv.index(f"--wallpaper") + 1
			if indexOfElement >= len(sys.argv) or sys.argv[indexOfElement].startswith("--"):
				piScreenUtils.logging.warning("No parameter given")
				verbose and print("No parameter given")
			else:
				if os.path.exists(sys.argv[indexOfElement]):
					piScreenUtils.logging.info(f"Set wallpaper to {os.path.abspath(sys.argv[indexOfElement])}")
					os.system(f'pcmanfm "--set-wallpaper={os.path.abspath(sys.argv[indexOfElement])}"')
				else:
					piScreenUtils.logging.warning("Wallpaper File dose't exist")
					verbose and print("Wallpaper File dose't exist")
		if f"--bg-color" in sys.argv:
			indexOfElement = sys.argv.index(f"--bg-color") + 1
			if indexOfElement >= len(sys.argv) or sys.argv[indexOfElement].startswith("--"):
				piScreenUtils.logging.warning("No parameter given")
				verbose and print("No parameter given")
			else:
				import re
				if re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', sys.argv[indexOfElement]):
					piScreenUtils.logging.info(f"Set backgroudcolor to {os.path.abspath(sys.argv[indexOfElement])}")
					desktopConfig = open("/home/pi/.config/pcmanfm/LXDE-pi/desktop-items-0.conf","r").readlines()
					count = 0
					found = False
					for i in desktopConfig:
						if i.startswith("desktop_bg="):
							desktopConfig[count] = f"desktop_bg={sys.argv[indexOfElement]}\n"
							found = True
						count = count + 1
					if not found:
						desktopConfig.append(f"desktop_bg={sys.argv[indexOfElement]}\n")
					open("/home/pi/.config/pcmanfm/LXDE-pi/desktop-items-0.conf","w").writelines(desktopConfig)
					os.system("pcmanfm --reconfigure")
				else:
					piScreenUtils.logging.warning("Given color is no valid hex string")
					verbose and print("Given color is no valid hex string")

	except:
		piScreenUtils.logging.warning("Error while access desktop configuration")
		verbose and print("Error while access desktop configuration")
		exit(1)

def getDekstopConfig():
	desktopJson = {}
	desktopConfig = open("/home/pi/.config/pcmanfm/LXDE-pi/desktop-items-0.conf","r").readlines()
	for i in desktopConfig:
		tmp = i.split("=")
		if len(tmp) > 1:
			desktopJson[tmp[0]] = tmp[1].replace("\n","")
	print(json.dumps(desktopJson))

def getStatus():
	import psutil
	verbose and print("Collect data")
	cpuLoad = round(psutil.getloadavg()[0] / psutil.cpu_count() * 100,2)
	ramTotal = round(psutil.virtual_memory().total / 1024)
	ramUsed = round(ramTotal - psutil.virtual_memory().available / 1024)
	upTime = time.time() - psutil.boot_time()
	cpuTemp = round(psutil.sensors_temperatures()["cpu_thermal"][0].current * 1000)
	screenshotTime = 0
	if os.path.isfile(piScreenUtils.paths.screenshot):
		screenshotTime = os.path.getctime(piScreenUtils.paths.screenshot)
	jsonData = {}
	jsonData["uptime"] = {}
	jsonData["uptime"]["secs"] = int(upTime % 60)
	jsonData["uptime"]["mins"] = int((upTime / 60) % 60)
	jsonData["uptime"]["hours"] = int((upTime / 60 / 60) % 24)
	jsonData["uptime"]["days"] = int(upTime / 60 / 60 / 24)
	jsonData["displayState"] = open(piScreenUtils.paths.displayStatus,"r").read().strip()
	jsonData["cpuTemp"] = cpuTemp
	jsonData["cpuLoad"] = cpuLoad
	jsonData["ramTotal"] = ramTotal
	jsonData["ramUsed"] = ramUsed
	jsonData["display"] = {}
	jsonData["display"]["standbySet"] = os.path.isfile(piScreenUtils.paths.displayStandby)
	jsonData["display"]["onSet"] = os.path.isfile(piScreenUtils.paths.displayOn)
	jsonData["screenshotTime"] = screenshotTime
	jsonData["modeInfo"] = {}
	jsonData["modeInfo"]["mode"] = getMode()
	if jsonData["modeInfo"]["mode"] == "firefox":
		try:
			if os.path.exists(piScreenUtils.paths.modeFirefox): jsonData["modeInfo"]["url"] = open(piScreenUtils.paths.modeFirefox,"r").read()
		except:
			piScreenUtils.logging.error("Error while reading firefox data")
			verbose and print("Error while reading Firefox data")
	elif jsonData["modeInfo"]["mode"] == "vlc":
		try:
			import telnetlib
			telnetClient = telnetlib.Telnet("127.0.0.1",9999)
			time.sleep(0.05)
			telnetClient.read_very_eager()
			
			telnetClient.write(b'status\n')
			time.sleep(0.05)
			result = telnetClient.read_very_eager().decode("utf-8")
			result = result.split("\r")
			if len(result) == 4:
				result1 = result[0][result[0].find("(")+2:result[0].find(")")-1]
				result2 = result[1][result[1].find("(")+2:result[1].find(")")-1]
				jsonData["modeInfo"]["source"] = result1[-len(result1)+result1.index(":")+2:]
				jsonData["modeInfo"]["volume"] = int(result2[-len(result2)+result2.index(":")+2:])
				jsonData["modeInfo"]["state"] = result[2][result[2].find("(")+2:result[2].find(")")-1].split(" ")[1]
			elif len(result) == 3:
				result1 = result[0][result[0].find("(")+2:result[0].find(")")-1]
				result2 = result[1][result[1].find("(")+2:result[1].find(")")-1]
				jsonData["modeInfo"]["volume"] = int(result1[-len(result1)+result1.index(":")+2:])
				jsonData["modeInfo"]["state"] = result[1][result[1].find("(")+2:result[1].find(")")-1].split(" ")[1]

			telnetClient.write(b'get_time\n')
			time.sleep(0.05)
			result = telnetClient.read_very_eager().decode("utf-8")
			result = result[:result.index("\r")]
			if piScreenUtils.isInt(result): jsonData["modeInfo"]["time"] = int(result)
			telnetClient.write(b'get_length\n')
			time.sleep(0.05)
			result = telnetClient.read_very_eager().decode("utf-8")
			result = result[:result.index("\r")]
			if piScreenUtils.isInt(result): jsonData["modeInfo"]["length"] = int(result)

		except:
			piScreenUtils.logging.error("Error while reading VLC data")
			verbose and print("Error while reading VLC data")
	elif jsonData["modeInfo"]["mode"] == "impress":
		try:
			if os.path.exists(piScreenUtils.paths.modeImpress): jsonData["modeInfo"]["file"] = open(piScreenUtils.paths.modeImpress,"r").read()
		except:
			piScreenUtils.logging.error("Error while reading impress data")
			verbose and print("Error while reading Impress data")
	return json.dumps(jsonData)

def getWebsite():
	if os.path.exists(piScreenUtils.paths.modeFirefox): print(open(piScreenUtils.paths.modeFirefox,"r").read())

def getMode():
	if os.path.exists(piScreenUtils.paths.modeFirefox):
		return "firefox"
	elif os.path.exists(piScreenUtils.paths.modeVLC):
		return "vlc"
	elif os.path.exists(piScreenUtils.paths.modeImpress):
		return "impress"
	return "none"

def screenOn():
	piScreenUtils.logging.info("Create file for turning on the screen")
	verbose and print("Create file for turning on the screen")
	open(piScreenUtils.paths.displayOn,"w").close()

def screenStandby():
	piScreenUtils.logging.info("Create file for turning screen to standby")
	verbose and print("Create file for turning screen to standby")
	open(piScreenUtils.paths.displayStandby,"w").close()

def screenOff():
	piScreenUtils.logging.info("Create file for turning off the screen")
	verbose and print("Create file for turning off the screen")
	open(piScreenUtils.paths.displayOff,"w").close()

def screenSwitchInput():
	piScreenUtils.logging.info("Create file for switching display input")
	verbose and print("Create file for switching display input")
	open(piScreenUtils.paths.displaySwitchChannel,"w").close()

def checkUpdate(draft,prerelease,silent):
	manifest = loadManifest()
	verbose and print(f"Current version {manifest['version']['major']}.{manifest['version']['minor']}.{manifest['version']['patch']}")
	latestRelease = getLatestVersion(draft,prerelease)
	if latestRelease:
		releaseVersion = latestRelease["tag_name"][1:].split(".")
		releaseVersion[0] = int(releaseVersion[0])
		releaseVersion[1] = int(releaseVersion[1])
		releaseVersion[2] = int(releaseVersion[2])
		if (
		manifest['version']['major'] < releaseVersion[0] or
		(manifest['version']['major'] == releaseVersion[0] and manifest['version']['minor'] < releaseVersion[1]) or
		(manifest['version']['major'] == releaseVersion[0] and manifest['version']['minor'] == releaseVersion[1] and manifest['version']['patch'] < releaseVersion[2])):
			if verbose:
				releaseChannel = "Stable"
				if latestRelease["prerelease"]:
					releaseChannel = "Pre-release"
				if latestRelease["draft"]:
					releaseChannel = "Draft"    
				print(f"New version {releaseVersion[0]}.{releaseVersion[1]}.{releaseVersion[2]} ({releaseChannel}) available")
			else:
				not silent and print(f"{releaseVersion[0]}.{releaseVersion[1]}.{releaseVersion[2]}")
			return latestRelease
		else:
			verbose and print("No new release available")
			return	
	else:
		verbose and print("No new release available")
		return	
	

def getLatestVersion(draft,prerelease):
	import requests
	releases = requests.get("https://api.github.com/repos/Jet0JLH/piScreen/releases")
	if releases.status_code != 200:
		verbose and print("Don't able to connect to Github API")
		return
	for release in releases.json():
		isPrerelease = release["prerelease"]
		isDraft = release["draft"]
		if not isDraft and not isPrerelease:
			#Stable Release
			return release
		elif isPrerelease and not isDraft:
			#Prerelease
			if prerelease or draft:
				return release
		elif isDraft:
			#Draft
			if draft:
				return release
	return

def downloadUpdate(draft,prerelease):
	import requests
	verbose and print("Check for updates")
	update = checkUpdate(draft,prerelease,True)
	if update:
		verbose and print("Download update")
		updateVersion = update["tag_name"][1:].split(".")
		downloadDir = f"/tmp/piScreen{updateVersion[0]}.{updateVersion[1]}.{updateVersion[2]}"
		os.path.isdir(downloadDir) and rmDir(downloadDir)
		os.mkdir(downloadDir)
		downloadUrl = ""
		for asset in update["assets"]:
			if asset["name"] == "install.zip" and asset["state"] == "uploaded":
				downloadUrl = asset["browser_download_url"]
				break
		if downloadUrl != "":
			verbose and print(downloadUrl)
			open(f"{downloadDir}/install.zip","wb").write(requests.get(downloadUrl).content)
			verbose and print("Download finished")
			verbose and print("Extract files")
			import zipfile
			with zipfile.ZipFile(f"{downloadDir}/install.zip", 'r') as installZip:
				installZip.extractall(downloadDir)
			verbose and print("Set rights for installation routine")
			os.system(f"chmod +x {downloadDir}/install/install.py")
			verbose and print("Start installation")
			import subprocess
			updateProcess = subprocess.Popen([f"{downloadDir}/install/install.py", "--update", "-y"])
			updateProcess.wait()
			updateProcess.returncode != 0 and verbose and print("Something went wrong during installation")
		else:
			piScreenUtils.logging.error("Something went wrong while downloading Updatefile")
			verbose and print("Something went wrong while downloading Updatefile")
		verbose and print("Cleanup installation")
		rmDir(downloadDir)
	else:
		verbose and print("Update not possible")

def rmDir(path):
	for root, dirs, files in os.walk(path, topdown=False):
		for name in files:
			os.remove(os.path.join(root, name))
		for name in dirs:
			os.rmdir(os.path.join(root, name))
	os.rmdir(path)

def setDisplayProtocol(protocol):
	piScreenUtils.logging.info(f"Set displayprotocol to {protocol}")
	protocol = protocol.lower()
	if protocol == "cec" or protocol == "ddc" or protocol == "manually":
		verbose and print(f"Write {protocol} as display protocol in settings.json")
		settingsJson = loadSettings()
		settingsJson["settings"]["display"]["protocol"] = protocol
		settingsFile = open(piScreenUtils.paths.settings, "w")
		settingsFile.write(json.dumps(settingsJson,indent=4))
		settingsFile.close()
		if os.path.exists(piScreenUtils.paths.displayCEC):
			os.remove(piScreenUtils.paths.displayCEC)
		if os.path.exists(piScreenUtils.paths.displayDDC):
			os.remove(piScreenUtils.paths.displayDDC)
		if os.path.exists(piScreenUtils.paths.displayMANUALLY):
			os.remove(piScreenUtils.paths.displayMANUALLY)
		if protocol == "cec":
			open(piScreenUtils.paths.displayCEC,"w").close()
		elif protocol == "ddc":
			open(piScreenUtils.paths.displayDDC,"w").close()
		elif protocol == "manually":
			open(piScreenUtils.paths.displayMANUALLY,"w").close()
	else:
		piScreenUtils.logging.warning(f"{protocol} is no permitted protocol")
		verbose and print(f"{protocol} is no permitted protocol")

def getDisplayProtocol():
	settingsJson = loadSettings()
	print(settingsJson["settings"]["display"]["protocol"])

def getDisplayOrientation():
	import subprocess
	orientation = subprocess.check_output("DISPLAY=:0 xrandr --query --verbose | grep HDMI-1 | cut -d ' ' -f 6",shell=True).decode("utf-8").replace("\n","")
	if orientation == "normal":
		return 0
	elif orientation == "right":
		return 1
	elif orientation == "inverted":
		return 2
	elif orientation == "left":
		return 3
	return None

def modifySchedule(element,typ,scheduleJson,elementName:str=""):
	if elementName == "": elementName = element
	changed = False
	if f"--{element}" in sys.argv:
		indexOfElement = sys.argv.index(f"--{element}") + 1
		if indexOfElement >= len(sys.argv) or sys.argv[indexOfElement].startswith("--"):
			try:
				del scheduleJson[elementName]
				changed = True
			except:
				pass
		else:
			if typ == bool:
				if sys.argv[indexOfElement].lower() == "true":
					scheduleJson[elementName] = True
					changed = True
				elif sys.argv[indexOfElement].lower() == "false":
					scheduleJson[elementName] = False
					changed = True
				else:
					piScreenUtils.logging.warning(f"{element} is not true or false")
					verbose and print(f"{element} is not true or false")
			elif typ == int:
				if piScreenUtils.isInt(sys.argv[indexOfElement]):
					scheduleJson[elementName] = int(sys.argv[indexOfElement])
					changed = True
				else:
					piScreenUtils.logging.warning(f"{element} is no number")
					verbose and print(f"{element} is no number")
			elif typ == datetime.datetime:
				try:
					datetime.datetime.strptime(sys.argv[indexOfElement], "%Y-%m-%d %H:%M")
					scheduleJson[elementName] = sys.argv[indexOfElement]
					changed = True
				except:
					piScreenUtils.logging.warning(f"{element} is no valid date")
					verbose and print(f"{element} is no valid date")
			elif typ == "pattern":
				if all(ch in "0123456789/-*, " for ch in sys.argv[indexOfElement]) and len(sys.argv[indexOfElement].split(" ")) == 5:
					scheduleJson[elementName] = sys.argv[indexOfElement]
					changed = True
				else:
					piScreenUtils.logging.warning(f"{element} is no valid pattern")
					verbose and print(f"{element} is no valid pattern")
			else:
				#Normal String without validation
				scheduleJson[elementName] = sys.argv[indexOfElement]
				changed = True
	return changed

def addCron():
	if i + 2 < len(sys.argv):
		if "--pattern" in sys.argv:
			pattern = sys.argv.index("--pattern") + 1
			if pattern < len(sys.argv):
				changed = False
				item = {}
				changed = modifySchedule("enabled",bool,item) or changed
				changed = modifySchedule("commandset",int,item) or changed
				changed = modifySchedule("start",datetime.datetime,item) or changed
				changed = modifySchedule("end",datetime.datetime,item) or changed
				changed = modifySchedule("pattern","pattern",item) or changed
				changed = modifySchedule("command",int,item) or changed
				changed = modifySchedule("parameter",None,item) or changed
				if changed:
					try:
						scheduleJson = loadSchedule()
						scheduleJson["cron"].append(item)
						scheduleFile = open(piScreenUtils.paths.schedule, "w")
						scheduleFile.write(json.dumps(scheduleJson,indent=4))
						scheduleFile.close()
						piScreenUtils.logging.info("Changed schedule.json")
						verbose and print("Changed schedule.json")
					except:
						piScreenUtils.logging.error("Error with schedule.json")
						verbose and print("Error with schedule.json")
						exit(1)
				else:
					piScreenUtils.logging.warning("Empty cron element")
					verbose and print("Empty cron element")
					exit(1)
			else:
				piScreenUtils.logging.warning("No pattern value")
				verbose and print("No pattern value")
				exit(1)
		else:
			piScreenUtils.logging.warning("Argument --pattern expected")
			verbose and print("Argument --pattern expected")
			exit(1)
	else:
		piScreenUtils.logging.warning("Not enough arguments")
		verbose and print("Not enough arguments")
		exit(1)

def updateCron():
	if i + 2 < len(sys.argv):
		if "--index" in sys.argv:
			index = sys.argv.index("--index") + 1
			if index < len(sys.argv):
				if piScreenUtils.isInt(sys.argv[index]):
					index = int(sys.argv[index])
					try:
						scheduleJson = loadSchedule()
						if index < len(scheduleJson["cron"]) and index >= 0:
							changed = False
							changed = modifySchedule("enabled",bool,scheduleJson["cron"][index]) or changed
							changed = modifySchedule("commandset",int,scheduleJson["cron"][index]) or changed
							changed = modifySchedule("start",datetime.datetime,scheduleJson["cron"][index]) or changed
							changed = modifySchedule("end",datetime.datetime,scheduleJson["cron"][index]) or changed
							changed = modifySchedule("pattern","pattern",scheduleJson["cron"][index]) or changed
							changed = modifySchedule("command",int,scheduleJson["cron"][index]) or changed
							changed = modifySchedule("parameter",None,scheduleJson["cron"][index]) or changed
							if changed:
								scheduleFile = open(piScreenUtils.paths.schedule, "w")
								scheduleFile.write(json.dumps(scheduleJson,indent=4))
								scheduleFile.close()
								piScreenUtils.logging.info("Changed schedule.json")
								verbose and print("Changed schedule.json")
						else:
							piScreenUtils.logging.warning("Index is bigger than count of cron entries")
							verbose and print("Index is bigger than count of cron entries")
							exit(1)
					except:
						piScreenUtils.logging.error("Error with schedule.json")
						verbose and print("Error with schedule.json")
						exit(1)
				else:
					piScreenUtils.logging.warning("Index is no number")
					verbose and print("Index is no number")
					exit(1)
			else:
				piScreenUtils.logging.warning("No index value")
				verbose and print("No index value")
				exit(1)
		else:
			piScreenUtils.logging.warning("Argument --index expected")
			verbose and print("Argument --index expected")
			exit(1)
	else:
		piScreenUtils.logging.warning("Not enough arguments")
		verbose and print("Not enough arguments")
		exit(1)

def addTrigger():
	if i + 2 < len(sys.argv):
		sys.argv.remove("--add-trigger")
		if "--trigger" in sys.argv:
			if piScreenUtils.isInt(sys.argv.index("--trigger") + 1):
				changed = False
				item = {}
				item["cases"] = {}
				changed = modifySchedule("enabled",bool,item) or changed
				changed = modifySchedule("trigger",int,item) or changed
				for i2 in sys.argv:
					if i2.startswith("--command:") and len(i2) > 10:
						if i2[i2.index(":")+1:] not in item["cases"]: item["cases"][i2[i2.index(":")+1:]] = {}
						changed = modifySchedule(i2[2:],int,item["cases"][i2[i2.index(":")+1:]],i2[2:i2.index(":")+1]) or changed
					elif i2.startswith("--parameter:") and len(i2) > 12:
						if i2[i2.index(":")+1:] not in item["cases"]: item["cases"][i2[i2.index(":")+1:]] = {}
						changed = modifySchedule(i2[2:],None,item["cases"][i2[i2.index(":")+1:]],i2[2:i2.index(":")+1]) or changed
					elif i2.startswith("--commandset:") and len(i2) > 13:
						if i2[i2.index(":")+1:] not in item["cases"]: item["cases"][i2[i2.index(":")+1:]] = {}
						changed = modifySchedule(i2[2:],int,item["cases"][i2[i2.index(":")+1:]],i2[2:i2.index(":")+1]) or changed
					elif i2.startswith("--") and i2 not in {"--enabled","--trigger","--"}:
						changed = modifySchedule(i2[2:],None,item) or changed
				if changed:
					try:
						scheduleJson = loadSchedule()
						scheduleJson["trigger"].append(item)
						scheduleFile = open(piScreenUtils.paths.schedule, "w")
						scheduleFile.write(json.dumps(scheduleJson,indent=4))
						scheduleFile.close()
						piScreenUtils.logging.info("Changed schedule.json")
						verbose and print("Changed schedule.json")
					except:
						piScreenUtils.logging.error("Error with schedule.json")
						verbose and print("Error with schedule.json")
						exit(1)
				else:
					piScreenUtils.logging.warning("Empty trigger element")
					verbose and print("Empty trigger element")
					exit(1)
			else:
				piScreenUtils.logging.warning("No pattern value")
				verbose and print("No pattern value")
				exit(1)
		else:
			piScreenUtils.logging.warning("Argument --trigger expected")
			verbose and print("Argument --trigger expected")
			exit(1)
	else:
		piScreenUtils.logging.warning("Not enough arguments")
		verbose and print("Not enough arguments")
		exit(1)

def updateTrigger():
	if i + 2 < len(sys.argv):
		sys.argv.remove("--update-trigger")
		if "--index" in sys.argv:
			index = sys.argv.index("--index") + 1
			if index < len(sys.argv):
				if piScreenUtils.isInt(sys.argv[index]):
					index = int(sys.argv[index])
					try:
						scheduleJson = loadSchedule()
						if index < len(scheduleJson["trigger"]) and index >= 0:
							item = scheduleJson["trigger"][index]
							changed = False
							changed = modifySchedule("enabled",bool,item) or changed
							changed = modifySchedule("trigger",int,item) or changed
							for i2 in sys.argv:
								if i2.startswith("--command:") and len(i2) > 10:
									if i2[i2.index(":")+1:] not in item["cases"]: item["cases"][i2[i2.index(":")+1:]] = {}
									changed = modifySchedule(i2[2:],int,item["cases"][i2[i2.index(":")+1:]],i2[2:i2.index(":")+1]) or changed
								elif i2.startswith("--parameter:") and len(i2) > 12:
									if i2[i2.index(":")+1:] not in item["cases"]: item["cases"][i2[i2.index(":")+1:]] = {}
									changed = modifySchedule(i2[2:],None,item["cases"][i2[i2.index(":")+1:]],i2[2:i2.index(":")+1]) or changed
								elif i2.startswith("--commandset:") and len(i2) > 13:
									if i2[i2.index(":")+1:] not in item["cases"]: item["cases"][i2[i2.index(":")+1:]] = {}
									changed = modifySchedule(i2[2:],int,item["cases"][i2[i2.index(":")+1:]],i2[2:i2.index(":")+1]) or changed
								elif i2.startswith("--") and i2 not in {"--index","--enabled","--trigger","--"}:
									changed = modifySchedule(i2[2:],None,item) or changed
							if changed:
								scheduleFile = open(piScreenUtils.paths.schedule, "w")
								scheduleFile.write(json.dumps(scheduleJson,indent=4))
								scheduleFile.close()
								piScreenUtils.logging.info("Changed schedule.json")
								verbose and print("Changed schedule.json")
						else:
							piScreenUtils.logging.warning("Index is bigger than count of trigger entries")
							verbose and print("Index is bigger than count of trigger entries")
							exit(1)
					except:
						piScreenUtils.logging.error("Error with schedule.json")
						verbose and print("Error with schedule.json")
						exit(1)
				else:
					piScreenUtils.logging.warning("Index is no number")
					verbose and print("Index is no number")
					exit(1)
			else:
				piScreenUtils.logging.warning("No index value")
				verbose and print("No index value")
				exit(1)
		else:
			piScreenUtils.logging.warning("Argument --index expected")
			verbose and print("Argument --index expected")
			exit(1)
	else:
		piScreenUtils.logging.warning("Not enough arguments")
		verbose and print("Not enough arguments")
		exit(1)

def addCommandset(update):
	if i + 2 < len(sys.argv):
		if "--name" in sys.argv or update:
			import random
			item = {}
			if update and modifySchedule("id",int,item):
				deleteCommandset()
			else:
				item["id"] = random.randint(100000,999999)
			modifySchedule("name",str,item)
			item["commands"] = []
			for x in range(len(sys.argv)):
				if sys.argv[x] == "--command":
					if len(sys.argv) > x + 2:
						if not sys.argv[x + 1].startswith("--"):
							if piScreenUtils.isInt(sys.argv[x + 1]):
								subitem = {}
								subitem["command"] = int(sys.argv[x + 1])
								if not sys.argv[x + 2].startswith("--"):
									subitem["parameter"] = sys.argv[x + 2]
								item["commands"].append(subitem)
					elif len(sys.argv) > x + 1:
						if not sys.argv[x + 1].startswith("--"):
							if piScreenUtils.isInt(sys.argv[x + 1]):
								subitem = {}
								subitem["command"] = int(sys.argv[x + 1])
								item["commands"].append(subitem)
			try:
				scheduleJson = loadSchedule()
				scheduleJson["commandsets"].append(item)
				scheduleFile = open(piScreenUtils.paths.schedule, "w")
				scheduleFile.write(json.dumps(scheduleJson,indent=4))
				scheduleFile.close()
				piScreenUtils.logging.info("Changed schedule.json")
				verbose and print("Changed schedule.json")
				print(item["id"])
			except:
				piScreenUtils.logging.error("Error with schedule.json")
				verbose and print("Error with schedule.json")
				exit(1)
		else:
			piScreenUtils.logging.warning("Argument --name expected")
			verbose and print("Argument --name expected")
			exit(1)
	else:
		piScreenUtils.logging.warning("Not enough arguments")
		verbose and print("Not enough arguments")
		exit(1)

def updateCommandset():
	if i + 2 < len(sys.argv):
		if "--id" in sys.argv:
			addCommandset(True)
		else:
			piScreenUtils.logging.warning("Argument --id expected")
			verbose and print("Argument --id expected")
			exit(1)
	else:
		piScreenUtils.logging.warning("Not enough arguments")
		verbose and print("Not enough arguments")
		exit(1)

def deleteCommandset():
	if i + 2 < len(sys.argv):
		if "--id" in sys.argv:
			if len(sys.argv) > sys.argv.index("--id") + 1 and piScreenUtils.isInt(sys.argv[sys.argv.index("--id") + 1]):
				try:
					found = False
					scheduleJson = loadSchedule()
					max = len(scheduleJson["commandsets"])
					for x in range(0,max):
						if "id" in scheduleJson["commandsets"][x]:
							if scheduleJson["commandsets"][x]["id"] == int(sys.argv[sys.argv.index("--id") + 1]):
								del scheduleJson["commandsets"][x]
								found = True
								max = max - 1
								break
					if found:
						scheduleFile = open(piScreenUtils.paths.schedule, "w")
						scheduleFile.write(json.dumps(scheduleJson,indent=4))
						scheduleFile.close()
						piScreenUtils.logging.info("Changed schedule.json")
						verbose and print("Changed schedule.json")
				except:
					piScreenUtils.logging.error("Error with schedule.json")
					verbose and print("Error with schedule.json")
					exit(1)
			else:
				piScreenUtils.logging.warning("Index is no number")
				verbose and print("Index is no number")
				exit(1)
		else:
			piScreenUtils.logging.warning("Argument --id expected")
			verbose and print("Argument --id expected")
			exit(1)
	else:
		piScreenUtils.logging.warning("Not enough arguments")
		verbose and print("Not enough arguments")
		exit(1)

#Main
verbose = False
sys.argv.pop(0) #Remove Path
if len(sys.argv) < 1:
	printHelp()

if "-v" in sys.argv:
    verbose = True
    sys.argv.remove("-v")

for i, origItem in enumerate(sys.argv):
	item = origItem.lower()
	if (
		item == "-h" or
		item == "--help"
	):
		printHelp()
	elif item == "--start-browser":
		if i + 1 < len(sys.argv):
			startBrowser(sys.argv[i + 1])
		else:
			piScreenUtils.logging.warning("Not enough arguments")
			verbose and print("Not enough arguments")
	elif item == "--restart-browser":
		restartBrowser()
	elif item == "--stop-browser":
		stopBrowser()
	elif item == "--start-vlc":
		if i + 1 < len(sys.argv):
			if getMode() == "vlc":
				try:
					import telnetlib
					piScreenUtils.logging.info("Change VLC source")
					telnetClient = telnetlib.Telnet("127.0.0.1",9999)
					telnetClient.write(bytes(f"clear\nadd {sys.argv[i + 1]}\n","utf-8"))
					startVLC(sys.argv[i + 1],True)
				except:
					piScreenUtils.logging.error("Not able to control VLC by telnet")
					verbose and print("Not able to control VLC by telnet")
					startVLC(sys.argv[i + 1])
			else:
				piScreenUtils.logging.info("Start VLC")
				startVLC(sys.argv[i + 1])
		else:
			piScreenUtils.logging.warning("Not enough arguments")
			verbose and print("Not enough arguments")
	elif item == "--restart-vlc":
		restartVLC()
	elif item == "--stop-vlc":
		stopVLC()
	elif item == "--pause-vlc":
		if getMode() == "vlc":
			import telnetlib
			telnetClient = telnetlib.Telnet("127.0.0.1",9999)
			telnetClient.write(b'pause\n')
		else:
			piScreenUtils.logging.warning("Mode is not VLC")
			verbose and print("Mode is not VLC")
	elif item == "--play-vlc":
		if getMode() == "vlc":
			import telnetlib
			telnetClient = telnetlib.Telnet("127.0.0.1",9999)
			telnetClient.write(b'play\n')
		else:
			piScreenUtils.logging.warning("Mode is not VLC")
			verbose and print("Mode is not VLC")
	elif item == "--start-impress":
		if i + 1 < len(sys.argv):
			startImpress(sys.argv[i + 1])
		else:
			piScreenUtils.logging.warning("Not enough arguments")
			verbose and print("Not enough arguments")
	elif item == "--restart-impress":
		restartImpress()
	elif item == "--stop-impress":
		stopImpress()
	elif item == "--reboot":
		reboot()
	elif item == "--shutdown":
		shutdown()
	elif item == "--configure-desktop":
		configureDesktop()
	elif item == "--get-desktop-configuration":
		getDekstopConfig()
	elif item == "--get-status":
		print(getStatus())
	elif item == "--screen-on":
		screenOn()
	elif item == "--screen-standby":
		screenStandby()
	elif item == "--screen-off":
		screenOff()
	elif item == "--screen-switch-input":
		screenSwitchInput()
	elif item == "--get-website":
		getWebsite()
	elif item == "--get-mode":
		print(getMode())
	elif item == "--set-pw":
		if i + 2 < len(sys.argv):
			if sys.argv[i + 2].lower() == "-f": #Check file Mode
				verbose and print("Set weblogin password with file")
				if i + 3 < len(sys.argv):
					if os.path.isfile(sys.argv[i + 3]):
						os.system(f"head -1 {sys.argv[i + 3]} | tr -d '\n' | sudo xargs -0 htpasswd -c -b /etc/apache2/.piScreen_htpasswd '{sys.argv[i + 1]}'")
						os.remove(sys.argv[i + 3])
					else:
						piScreenUtils.logging.error("Passwortfile dosn't exist")
						verbose and print("Passwordfile doesn't exist")
				else:
					piScreenUtils.logging.error("No passwordfile specified")
					verbose and print("No passwordfile specified")
			else: #Check direct mode
				verbose and print("Set weblogin password with next parameter")
				os.system(f"sudo htpasswd -c -b /etc/apache2/.piScreen_htpasswd '{sys.argv[i + 1]}' '{sys.argv[i + 2]}'")
		else:
			piScreenUtils.logging.warning("Not enough arguments")
			verbose and print("Not enough arguments")
	elif item == "--check-update":
		prerelease = False
		draft = False
		if i + 2 < len(sys.argv):
			if sys.argv[i + 2].lower() == "--draft":
				draft = True
			elif sys.argv[i + 2].lower() == "--pre-release":
				prerelease = True
		if i + 1 < len(sys.argv):
			if sys.argv[i + 1].lower() == "--draft":
				draft = True
			elif sys.argv[i + 1].lower() == "--pre-release":
				prerelease = True
		
		checkUpdate(draft,prerelease,False)
	elif item == "--do-upgrade":
		not checkForRootPrivileges() and sys.exit(1)
		prerelease = False
		draft = False
		if i + 2 < len(sys.argv):
			if sys.argv[i + 2].lower() == "--draft":
				draft = True
			elif sys.argv[i + 2].lower() == "--pre-release":
				prerelease = True
		if i + 1 < len(sys.argv):
			if sys.argv[i + 1].lower() == "--draft":
				draft = True
			elif sys.argv[i + 1].lower() == "--pre-release":
				prerelease = True
		downloadUpdate(draft,prerelease)
	elif item == "--set-display-protocol":
		if i + 1 < len(sys.argv):
			setDisplayProtocol(sys.argv[i + 1])
		else:
			piScreenUtils.logging.warning("Not enough arguments")
			verbose and print("Not enough arguments")
	elif item == "--get-display-protocol":
		getDisplayProtocol()
	elif item == "--set-display-orientation":
		saveSettings = True
		if "--no-save" in sys.argv:
			saveSettings = False
			sys.argv.remove("--no-save")
		if i + 1 < len(sys.argv):
			found = False
			if sys.argv[i + 1] == "0":
				found = True
				os.system("DISPLAY=:0 xrandr -o normal")
				piScreenUtils.logging.info("Change displayorientation to normal")
				verbose and print("Change displayorientation to normal")
			elif sys.argv[i + 1] == "1":
				found = True
				os.system("DISPLAY=:0 xrandr -o right")
				piScreenUtils.logging.info("Change displayorientation to right")
				verbose and print("Change displayorientation to right")
			elif sys.argv[i + 1] == "2":
				found = True
				os.system("DISPLAY=:0 xrandr -o inverted")
				piScreenUtils.logging.info("Change displayorientation to inverted")
				verbose and print("Change displayorientation to inverted")
			elif sys.argv[i + 1] == "3":
				found = True
				os.system("DISPLAY=:0 xrandr -o left")
				piScreenUtils.logging.info("Change displayorientation to left")
				verbose and print("Change displayorientation to left")
			if found and saveSettings:
				settingsJson = loadSettings()
				settingsJson["settings"]["display"]["orientation"] = int(sys.argv[i + 1])
				settingsFile = open(piScreenUtils.paths.settings, "w")
				settingsFile.write(json.dumps(settingsJson,indent=4))
				settingsFile.close()
				piScreenUtils.logging.info("Write orientation in settings")
				verbose and print("Write orientation in settings")
		else:
			piScreenUtils.logging.warning("Not enough arguments")
			verbose and print("Not enough arguments")
	elif item == "--get-display-orientation-settings":
		settingsJson = loadSettings()
		try:
			print(settingsJson["settings"]["display"]["orientation"])
		except:
			piScreenUtils.logging.error("Can not read displayorientation from settings")
			print(0)
	elif item == "--get-display-orientation":
		print(getDisplayOrientation())
	elif item == "--schedule-firstrun":
		piScreenUtils.logging.info("Write file for schedule firstrun")
		open(piScreenUtils.paths.scheduleDoFirstRun,"w").close()
	elif item == "--schedule-lastcron":
		piScreenUtils.logging.info("Write file for schedule last cron")
		open(piScreenUtils.paths.scheduleDoLastCron,"w").close()
	elif item == "--schedule-manually-command":
		if i + 2 < len(sys.argv):
			if sys.argv[i + 1] == "--command":
				if piScreenUtils.isInt(sys.argv[i + 2]):
					command = {}
					command["type"] = "command"
					command["command"] = int(sys.argv[i + 2])
					if i + 4 < len(sys.argv):
						if sys.argv[i + 3] == "--parameter":
							command["parameter"] = sys.argv[i + 4]
						else:
							piScreenUtils.logging.warning("Missing parameter flag")
							verbose and print("Missing parameter flag")
							exit(1)
					piScreenUtils.logging.info("Create file for manually command run")
					manualFile = open(piScreenUtils.paths.scheduleDoManually, "w")
					manualFile.write(json.dumps(command))
					manualFile.close()
				else:
					piScreenUtils.logging.warning("Command is no number")
					verbose and print("Command is no number")
					exit(1)
			else:
				piScreenUtils.logging.warning("Argument --command expected")
				verbose and print("Argument --command expected")
				exit(1)
		else:
			piScreenUtils.logging.warning("Not enough arguments")
			verbose and print("Not enough arguments")
			exit(1)
	elif item == "--schedule-manually-commandset":
		if i + 2 < len(sys.argv):
			if sys.argv[i + 1] == "--id":
				if piScreenUtils.isInt(sys.argv[i + 2]):
					piScreenUtils.logging.info("Create file for manually commandset run")
					manualFile = open(piScreenUtils.paths.scheduleDoManually, "w")
					manualFile.write(json.dumps({"type":"commandset","id":int(sys.argv[i + 2])},indent=4))
					manualFile.close()
				else:
					piScreenUtils.logging.warning("Index is no number")
					verbose and print("Index is no number")
					exit(1)
			else:
				piScreenUtils.logging.warning("Argument --index expected")
				verbose and print("Argument --index expected")
				exit(1)
		else:
			piScreenUtils.logging.warning("Not enough arguments")
			verbose and print("Not enough arguments")
			exit(1)
	elif item == "--schedule-manually-cron":
		if i + 2 < len(sys.argv):
			if sys.argv[i + 1] == "--index":
				if piScreenUtils.isInt(sys.argv[i + 2]):
					piScreenUtils.logging.info("Create file for manually cron run")
					manualFile = open(piScreenUtils.paths.scheduleDoManually, "w")
					manualFile.write(json.dumps({"type":"cron","index":int(sys.argv[i + 2])},indent=4))
					manualFile.close()
				else:
					piScreenUtils.logging.warning("Index is no number")
					verbose and print("Index is no number")
					exit(1)
			else:
				piScreenUtils.logging.warning("Argument --index expected")
				verbose and print("Argument --index expected")
				exit(1)
		else:
			piScreenUtils.logging.warning("Not enough arguments")
			verbose and print("Not enough arguments")
			exit(1)
	elif item == "--schedule-manually-trigger":
		if i + 2 < len(sys.argv):
			if sys.argv[i + 1] == "--index":
				if piScreenUtils.isInt(sys.argv[i + 2]):
					piScreenUtils.logging.info("Create file for manually trigger run")
					manualFile = open(piScreenUtils.paths.scheduleDoManually, "w")
					manualFile.write(json.dumps({"type":"trigger","index":int(sys.argv[i + 2])},indent=4))
					manualFile.close()
				else:
					piScreenUtils.logging.warning("Index is no number")
					verbose and print("Index is no number")
					exit(1)
			else:
				piScreenUtils.logging.warning("Argument --index expected")
				verbose and print("Argument --index expected")
				exit(1)
		else:
			piScreenUtils.logging.warning("Not enough arguments")
			verbose and print("Not enough arguments")
			exit(1)
	elif item == "--add-cron":
		addCron()
	elif item == "--update-cron":
		updateCron()
	elif item == "--delete-cron":
		if i + 2 < len(sys.argv):
			if sys.argv[i + 1] == "--index":
				if piScreenUtils.isInt(sys.argv[i + 2]):
					try:
						scheduleJson = loadSchedule()
						index = int(sys.argv[i + 2])
						if index < len(scheduleJson["cron"]) and index >= 0:
							del scheduleJson["cron"][index]
							scheduleFile = open(piScreenUtils.paths.schedule, "w")
							scheduleFile.write(json.dumps(scheduleJson,indent=4))
							scheduleFile.close()
							piScreenUtils.logging.info("Changed schedule.json")
							verbose and print("Changed schedule.json")
						else:
							piScreenUtils.logging.warning("Index is bigger than count of cron entries")
							verbose and print("Index is bigger than count of cron entries")
							exit(1)
					except:
						piScreenUtils.logging.error("Error with schedule.json")
						verbose and print("Error with schedule.json")
						exit(1)
				else:
					piScreenUtils.logging.warning("Index is no number")
					verbose and print("Index is no number")
					exit(1)
			else:
				piScreenUtils.logging.warning("Argument --index expected")
				verbose and print("Argument --index expected")
				exit(1)
		else:
			piScreenUtils.logging.warning("Not enough arguments")
			verbose and print("Not enough arguments")
			exit(1)
	elif item == "--add-commandset":
		addCommandset(False)
	elif item == "--update-commandset":
		updateCommandset()
	elif item == "--delete-commandset":
		deleteCommandset()
	elif item == "--add-trigger":
		addTrigger()
	elif item == "--update-trigger":
		updateTrigger()
	elif item == "--delete-trigger":
		if i + 2 < len(sys.argv):
			if sys.argv[i + 1] == "--index":
				if piScreenUtils.isInt(sys.argv[i + 2]):
					try:
						scheduleJson = loadSchedule()
						index = int(sys.argv[i + 2])
						if index < len(scheduleJson["trigger"]) and index >= 0:
							del scheduleJson["trigger"][index]
							scheduleFile = open(piScreenUtils.paths.schedule, "w")
							scheduleFile.write(json.dumps(scheduleJson,indent=4))
							scheduleFile.close()
							piScreenUtils.logging.info("Changed schedule.json")
							verbose and print("Changed schedule.json")
						else:
							piScreenUtils.logging.warning("Index is bigger than count of tigger entries")
							verbose and print("Index is bigger than count of trigger entries")
							exit(1)
					except:
						piScreenUtils.logging.error("Error with schedule.json")
						verbose and print("Error with schedule.json")
						exit(1)
				else:
					piScreenUtils.logging.warning("Index is no number")
					verbose and print("Index is no number")
					exit(1)
			else:
				piScreenUtils.logging.warning("Argument --index expected")
				verbose and print("Argument --index expected")
				exit(1)
		else:
			piScreenUtils.logging.warning("Not enough arguments")
			verbose and print("Not enough arguments")
			exit(1)