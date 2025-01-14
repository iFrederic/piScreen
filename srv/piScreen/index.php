<!doctype html>
<html>
    <head>
        <link rel='stylesheet' href='/bootstrap/icons/bootstrap-icons.css'>
		<link rel='stylesheet' href='default.css'>
		<title>piScreen Defaultpage</title>
    </head>
    <body>
    <?php exec("ip route | grep default | sed -e 's/^.* src \([^ ]*\) .*$/\\1/'", $ip); ?>
        <center>
            <div>
                <div class='imgbox'>
                    <img src='/piScreen.svg' alt='Logo' width='30%' height='30%'>
                </div>
                <h2>🥳 You successfully installed piScreen 🎉</h2>
            </div>
            <div class='importantInfo'>
                <p style='margin: 0;'>To administer your screen, please visit <a href="https://<?php echo $ip[0];?>/admin">https://<?php echo $ip[0];?>/admin</a></p>
            </div>
            <div>
                <table>
                    <tr>
                        <td>
                            <div class='card'>
                                <i class='bi-exclamation-triangle bigIcon'></i><br>
                                <p><u>Observe:</u></p>
                                <ul>
                                    <li>Display status</li>
                                    <li>Uptime</li>
                                    <li>CPU load</li>
                                    <li>CPU temperature</li>
                                    <li>And more...</li>
                                </ul>
                            </div>
                        </td>
                        <td>
                            <div class='card'>
                                <i class='bi-boxes bigIcon'></i><br>
                                <p><u>Administer:</u></p>
                                <ul>
                                    <li>Reboot  Pi</li>
                                    <li>Shutdown  Pi</li>
                                    <li>Toggle display state</li>
                                    <li>Filemanager</li>
                                    <li>Modify commandsets</li>
                                    <li>Modify trigger</li>
                                </ul>
                            </div>
                        </td>
                        <td>
                            <div class='card'>
                                <i class='bi-gear bigIcon'></i><br>
                                <p><u>Configure:</u></p>
                                <ul>
                                    <li>Hostname</li>
                                    <li>Display protocol</li>
                                    <li>Display orientation</li>
                                    <li>Desktop background</li>
                                    <li>Import / export time schedule</li>
                                </ul>
                            </div>
                        </td>
                        <td>
                            <div class='card'>
                                <i class='bi-calendar2-day bigIcon'></i><br>
                                <p><u>Plan:</u></p>
                                <ul>
                                    <li>General commands</li>
                                    <li>Display control</li>
                                    <li>Firefox control</li>
                                    <li>VLC control</li>
                                    <li>Impress control</li>
                                    <li>Individual commandsets</li>
                                </ul>
                            </div>
                        </td>
                   </tr>
                </table>
            </div>
            <div class='footer'>
                <p class="grayed smallerText"> <i class='bi bi-pc-display'></i> Hostname: <?php echo gethostname(); ?></p>
                <p class="grayed smallerText">piScreen is provided by Jet0JLH and toefde. <i class='bi-github'></i> The project can be found on GitHub: <u>https://github.com/Jet0JLH/piScreen</u>
            </div>
        </center>
    </body>
</html>