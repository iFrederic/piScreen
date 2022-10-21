#!/bin/bash
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"
touch /media/ramdisk/piScreenDisplayOn
touch /media/ramdisk/piScreenDisplaySwitch
touch /media/ramdisk/piScreenScheduleActive
rm /media/ramdisk/piScreenDisplayCEC
rm /media/ramdisk/piScreenDisplayDDC

protocol=$(cat /home/pi/piScreen/settings.json | grep '\"protocol\"\s*:\s*\"' | cut -f2- -d:)
if [ $protocol == "\"cec\"" ] ; then
	touch /media/ramdisk/piScreenDisplayCEC
elif [ $protocol == "\"ddc\"" ] ; then
	touch /media/ramdisk/piScreenDisplayDDC
fi
sleep 10
export DISPLAY=:0
browser=firefox-esr
browserPID=$(pgrep -x $browser)

unclutter -idle 5 &
./piScreenDisplay.sh &
displayPID=$!
./piScreenScreenshot.py &
screenshotPID=$!

while [ true ] ; do
	kill -0 $browserPID
	if [ $? -gt 0 ] ; then
		./piScreenCmd.py --start-browser
		sleep 5
		browserPID=$(pgrep -x $browser)
	fi
	kill -0 $displayPID
	if [ $? -gt 0 ] ; then
		./piScreenDisplay.sh &
		displayPID=$!
		sleep 5
	fi
	kill -0 $screenshotPID
	if [ $? -gt 0 ] ; then
		./piScreenScreenshot.py &
		screenshotPID=$!
		sleep 5
	fi
	sleep 1
done
