<?php
	$sudoSyscall = 'sudo /home/pi/piScreen/piScreenCmd.py';
	$syscall = 'sudo -u pi /home/pi/piScreen/piScreenCmd.py';
	$fileExplorerPath = "/srv/piScreen/admin/data/";
	$modes = ["general", "firefox", "vlc", "impress"];

	function executeCommand($command, $sendResponse) {
		try {
			exec($command, $returnval, $returncode);
		} catch (Exception $e) {
			$returnval = strval($e);
		}
		if ($sendResponse) {
			sendResponse($returnval, $returncode);
		}
	}

	function sendResponse($returnval, $returncode) {
		if (is_array($returnval)) {
			echo implode(":;:", $returnval) . ":-:" . $returncode;
		} else {
			echo $returnval . ":-:" . $returncode;
		}
	}

	if ($_GET['id'] == 1) { //Firefox
		if ($_GET['cmd'] == "restart") {
			executeCommand("$syscall --do-firefox-restart", true);
		} elseif ($_GET['cmd'] == "refresh") {
			executeCommand("$syscall --do-firefox-refresh", true);
		}
	}
	elseif ($_GET['id'] == 2) { //reboot
		executeCommand("$sudoSyscall --do-reboot", false);
	}
	elseif ($_GET['id'] == 3) { //Shutdown
		executeCommand("$sudoSyscall --do-shutdown", false);
	}
	elseif ($_GET['id'] == 4) {//Change hostname
		$hostname = shell_exec('hostname');
		if($hostname != $_POST['hostname']) {
			executeCommand("sudo hostnamectl set-hostname '{$_POST['hostname']}'", true);
		} else {//already correct hostname set
			sendResponse("", 0);
		}
	}
	elseif ($_GET['id'] == 5) { //Get Infos
		header("Content-Type: application/json; charset=UTF-8");
		executeCommand("$syscall --get-status", true);
	}
	elseif ($_GET['id'] == 6) { //Check for update
		executeCommand("$syscall --check-update", true);
	}
	elseif ($_GET['id'] == 7) { //Set weblogin
		if($_POST['user'] && $_POST['pwd']) {
			executeCommand("$syscall --set-password '" . $_POST['user'] . "' '" . $_POST['pwd'] . "'", true);
		}
	}
	elseif ($_GET['id'] == 8) { //Display Control
		if ($_GET['cmd'] == 1) {
			executeCommand("$syscall --set-display on", true);
		}
		elseif ($_GET['cmd'] == 2) {
			executeCommand("$syscall --set-display off", true);
		}
		elseif ($_GET['cmd'] == 3) {
			executeCommand("$syscall --set-display-input", true);
		}
	}
	elseif ($_GET['id'] == 9) { //Set Schedule
		if ($_GET['cmd'] == "add"){
			$parameterString = "";
			if ($_GET['enabled'] != NULL) {
				$parameterString .= " --enabled " . $_GET['enabled'];
			}
			if ($_GET['command'] != NULL) {
				$parameterString .= " --command " . $_GET['command'];
			}
			if ($_GET['parameter'] != NULL) {
				$parameterString .= " --parameter " . $_GET['parameter'];
			}
			if ($_GET['start'] != NULL) {
				$parameterString .= " --start \"" . $_GET['start'] . "\"";
			}
			if ($_GET['end'] != NULL) {
				$parameterString .= " --end \"" . $_GET['end'] . "\"";
			}
			if ($_GET['pattern'] != NULL) {
				$parameterString .= " --pattern \"" . $_GET['pattern'] . "\"";
			}
			if ($_GET['commandset'] != NULL) {
				$parameterString .= " --commandset " . $_GET['commandset'];
			}
			executeCommand("$syscall --add-cron-entry$parameterString", true);

		} elseif ($_GET['cmd'] == "update") {
			$parameterString = " --index " . $_GET['index'];
			if ($_GET['enabled'] != NULL) {
				$parameterString .= " --enabled " . $_GET['enabled'];
			}
			if ($_GET['command'] != NULL) {
				$parameterString .= " --command " . $_GET['command'];
			}
			if ($_GET['parameter'] != NULL) {
				$parameterString .= " --parameter " . $_GET['parameter'];
			}
			if ($_GET['start'] == " ") {
				$parameterString .= " --start";
			} elseif ($_GET['start'] != NULL) {
				$parameterString .= " --start \"" . $_GET['start'] . "\"";
			}
			if ($_GET['end'] == " ") {
				$parameterString .= " --end";
			} elseif ($_GET['end'] != NULL) {
				$parameterString .= " --end \"" . $_GET['end'] . "\"";
			}
			if ($_GET['pattern'] != NULL) {
				$parameterString .= " --pattern \"" . $_GET['pattern'] . "\"";
			}
			if ($_GET['commandset'] != NULL) {
				$parameterString .= " --commandset " . $_GET['commandset'];
			}
			executeCommand("$syscall --update-cron-entry$parameterString", true);

		} elseif ($_GET['cmd'] == "delete") {
			$parameterString = " --index " . $_GET['index'];
			executeCommand("$syscall --delete-cron-entry$parameterString", true);
		} elseif ($_GET['cmd'] == "execute") {
			$parameterString = " --index " . $_GET['index'];
			executeCommand("$syscall --run-cron-manually$parameterString", true);
		}
	}
	elseif ($_GET['id'] == 10) { //Get time schedule
		try {
			header("Content-Type: application/json; charset=UTF-8");
			sendResponse(file_get_contents('/home/pi/piScreen/schedule.json'), 0);//send directly because it is a json file
		} catch (Exception $e) {
			sendResponse($e, 1);
		}
	}
	elseif ($_GET['id'] == 11) { //Get manifest
		try {
			header("Content-Type: application/json; charset=UTF-8");
			sendResponse(file_get_contents('/home/pi/piScreen/manifest.json'), 0);
		} catch (Exception $e) {
			sendResponse($e, 1);
		}
	}
	elseif ($_GET['id'] == 12) { //Get settings
		try {
			header("Content-Type: application/json; charset=UTF-8");
			sendResponse(file_get_contents('/home/pi/piScreen/settings.json'), 0);
		} catch (Exception $e) {
			sendResponse($e, 1);
		}
	}
	elseif ($_GET['id'] == 13) { //Set language
		executeCommand("$syscall --set-language " . $_GET['lang'], true);
	}
	elseif ($_GET['id'] == 14) { //Set diplay control protocol
		if ($_GET['protocol'] == 'cec') {
			executeCommand("$syscall --set-display-protocol cec", true);
		}
		elseif ($_GET['protocol'] == 'ddc') {
			executeCommand("$syscall --set-display-protocol ddc", true);
		}
		elseif ($_GET['protocol'] == 'manually') {
			executeCommand("$syscall --set-display-protocol manually", true);
		}
	}
	elseif ($_GET['id'] == 15) { //Get display control protocol
		executeCommand("$syscall --get-display-protocol", true);
	}
	elseif ($_GET['id'] == 16) { //Set diplay orientation
		$orientation = $_GET['orientation'];
		if ($orientation >= 0 && $orientation <= 3) {
			executeCommand("$syscall --set-display-orientation $orientation", true);
		}
	}
	elseif ($_GET['id'] == 17) { //Get diplay orientation
		executeCommand("$syscall --get-display-orientation --settings", true);
	}
	elseif ($_GET['id'] == 18) { //Set entire schedule
		try {
			file_put_contents('/home/pi/piScreen/schedule.json', file_get_contents('php://input'));
		} catch (Exception $e) {
			sendResponse($e, 1);
		}
		sendResponse("", 0);
	}
	elseif ($_GET['id'] == 19) { //commandset functions
		if ($_GET['cmd'] == "add"){
			$parameterString = " --description " . $_GET['description'];
			for ($id = 0; true; $id++) {
				if ($_GET['command' . $id] != NULL) {
					$parameterString .= " --command " . $_GET['command' . $id];
					if ($_GET['parameter' . $id] != NULL) {
						$parameterString .= " " . $_GET['parameter' . $id];
					}
				} else {
					break;
				}
			}
			//echo "$syscall --add-commandset$parameterString";
			executeCommand("$syscall --add-commandset-entry$parameterString", true);
		} elseif ($_GET['cmd'] == "update") {
			$parameterString .= " --id " . $_GET['commandsetid'];
			if ($_GET['description'] != NULL) {
				$parameterString .= " --description " . $_GET['description'];
			}
			for ($id = 0; true; $id++) {
				if ($_GET['command' . $id] != NULL) {
					$parameterString .= " --command " . $_GET['command' . $id];
					if ($_GET['parameter' . $id] != NULL) {
						$parameterString .= " " . $_GET['parameter' . $id];
					}
				} else {
					break;
				}
			}
			executeCommand("$syscall --update-commandset-entry$parameterString", true);
		} elseif ($_GET['cmd'] == "delete") {
			$parameterString = " --id " . $_GET['commandsetid'];
			executeCommand("$syscall --delete-commandset-entry$parameterString", true);
		} elseif ($_GET['cmd'] == "execute") {
			$parameterString = " --id " . $_GET['commandsetid'];
			executeCommand("$syscall --run-commandset-manually$parameterString", true);
		}
	}
	elseif ($_GET['id'] == 20) { //Trigger functions
		if ($_GET['cmd'] == "add"){
			$parameterString = "";
			if ($_GET['enabled'] != NULL) {
				$parameterString .= " --enabled " . $_GET['enabled'];
			}
			if ($_GET['trigger'] != NULL) {
				$parameterString .= " --trigger " . $_GET['trigger'];
			}
			if ($_GET['description'] != NULL) {
				$parameterString .= " --description " . $_GET['description'];
			}
			$cases = $_GET["cases"];
			for ($i = 0; $i < count($cases); $i++) {
				if ($_GET['command' . $cases[$i]] != NULL) {
					$parameterString .= " --command:" . $_GET['command' . $cases[$i]];
				}
				if ($_GET['parameter' . $cases[$i]] != NULL) {
					$parameterString .= " --parameter:" . $_GET['parameter' . $cases[$i]];
				}
				if ($_GET['commandset' . $cases[$i]] != NULL) {
					$parameterString .= " --commandset:" . $_GET['commandset' . $cases[$i]];
				}
			}
			$triggerParameter = $_GET["triggerParameter"];
			for ($i = 0; $i < count($triggerParameter); $i++) {
				$parameterString .= " --" . $triggerParameter[$i];
			}
			echo "$syscall --add-trigger-entry$parameterString";
			executeCommand("$syscall --add-trigger-entry$parameterString", true);

		} elseif ($_GET['cmd'] == "update") {
			$parameterString = " --index " . $_GET['index'];
			if ($_GET['enabled'] != NULL) {
				$parameterString .= " --enabled " . $_GET['enabled'];
			}
			if ($_GET['trigger'] != NULL) {
				$parameterString .= " --trigger " . $_GET['trigger'];
			}
			if ($_GET['description'] != NULL) {
				$parameterString .= " --description " . $_GET['description'];
			}
			$cases = $_GET["cases"];
			for ($i = 0; $i < count($cases); $i++) {
				if ($_GET['command' . $cases[$i]] != NULL) {
					$parameterString .= " --command:" . $_GET['command' . $cases[$i]];
				}
				if ($_GET['parameter' . $cases[$i]] != NULL) {
					$parameterString .= " --parameter:" . $_GET['parameter' . $cases[$i]];
				}
				if ($_GET['commandset' . $cases[$i]] != NULL) {
					$parameterString .= " --commandset:" . $_GET['commandset' . $cases[$i]];
				}
			}
			$triggerParameter = $_GET["triggerParameter"];
			for ($i = 0; $i < count($triggerParameter); $i++) {
				$parameterString .= " --" . $triggerParameter[$i];
			}
			//echo "$syscall --update-trigger$parameterString";
			executeCommand("$syscall --update-trigger-entry$parameterString", true);

		} elseif ($_GET['cmd'] == "delete") {
			$parameterString = " --index " . $_GET['index'];
			//echo "$syscall --delete-trigger$parameterString";
			executeCommand("$syscall --delete-trigger-entry$parameterString", true);

		} elseif ($_GET['cmd'] == "execute") {
			$parameterString = " --index " . $_GET['index'];
			executeCommand("$syscall --run-trigger-manually$parameterString", true);
		}
	}
	elseif ($_GET['id'] == 21) { //export schedule
		header("Content-Type: application/json; charset=UTF-8");
		echo file_get_contents('/home/pi/piScreen/schedule.json');
	}
	elseif ($_GET['id'] == 22) { //Run lastcron
		executeCommand("$syscall --run-lastcron", true);
	}
	elseif ($_GET['id'] == 23) { //Run firstrun
		executeCommand("$syscall --run-firstrun", true);
	}
	elseif ($_GET['id'] == 24) { //Get files for file explorer
		$fileArray = scandir($fileExplorerPath . $modes[$_GET['mode']]);
		$fileArray = array_diff($fileArray, [".", ".."]);
		sendResponse($fileArray, 0);
	}
	elseif ($_GET['id'] == 25) { //Upload files for file explorer
		try {
			$location = $fileExplorerPath . $modes[$_GET['mode']] . "/" . $_FILES['file']['name'];
			move_uploaded_file($_FILES['file']['tmp_name'], $location);
		} catch (\Throwable $th) {
			sendResponse("Unable to upload file", 1);
		}
		sendResponse("", 0);
	}
	elseif ($_GET['id'] == 26) { //Delete files for file explorer
		try {
			unlink($fileExplorerPath . $modes[$_GET['mode']] . "/" . $_GET['filename']);
		} catch (\Throwable $th) {
			sendResponse("Unable to delete file", 1);
		}
		sendResponse("", 0);
	}
	elseif ($_GET['id'] == 27) { //Rename file for file explorer
		try {
			rename($fileExplorerPath . $modes[$_GET['mode']] . "/" . $_GET['oldfilename'], $fileExplorerPath . $modes[$_GET['mode']] . "/" . $_GET['newfilename']);
		} catch (\Throwable $th) {
			sendResponse("Unable to rename file", 1);
		}
		sendResponse("", 0);
	}
	elseif ($_GET['id'] == 28) { //VLC
		if ($_GET['cmd'] == "restart") {
			executeCommand("$syscall --do-vlc-restart", true);
		} elseif ($_GET['cmd'] == "play") {
			executeCommand("$syscall --do-vlc-play", true);
		} elseif ($_GET['cmd'] == "pause") {
			executeCommand("$syscall --do-vlc-pause", true);
		} elseif ($_GET['cmd'] == "volume") {
			executeCommand("$syscall --set-vlc-volume " . $_GET['value'], true);
		}
	}
	elseif ($_GET['id'] == 29) { //Impress
		executeCommand("$syscall --do-impress-restart", true);
	}
	elseif ($_GET['id'] == 30) { //Get background
		executeCommand("$syscall --get-desktop-configuration", true);
	}
	elseif ($_GET['id'] == 31) { //Set background mode
		executeCommand("$syscall --set-desktop-configuration --mode " . $_GET["mode"], true);
	}
	elseif ($_GET['id'] == 32) { //Set background color
		executeCommand("$syscall --set-desktop-configuration --background-color \\#" . $_GET["color"], true);
	}
	elseif ($_GET['id'] == 33) { //Set background wallpaper
		executeCommand("$syscall --set-desktop-configuration --wallpaper \"" . $_GET["path"] . "\"", true);
	}
	elseif ($_GET['id'] == 34) { //Set ignore time schedule
		executeCommand("$syscall --set-cron-ignore-timespan " . $_GET["fromto"], true);
	}
	elseif ($_GET['id'] == 35) { //Execute command once
		$parameterString = "$syscall --run-command-manually --command " . $_GET["commandid"];
		if ($_GET["parameter"]) {
			$parameterString .= " --parameter " . $_GET["parameter"];
		}
		executeCommand($parameterString, true);
	}
?>
