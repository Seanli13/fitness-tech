# fitness-tech

Given this project's use of the PyAudio library, we have to include the snippet before the python command in the cron job. This is because the Pulse Audio system in Bullseye doesn't start until after the user has logged in, which occurs after the cronjob execution. This means that, without the extra snippet, the program runs fine when run from command line, but not via cron reboot.
@reboot XDG_RUNTIME_DIR=/run/user/$(id -u) python3 /home/sean/Desktop/fitness-tech/main.py >> /home/sean/Desktop/testing.log 2>&1

# Enable autorun
1. To run BlindVision fitness automatically on reboot, you must first open the RPi either through desktop or SSH/VNC.
2. Open the terminal if you haven't already
3. Enter the following command: **crontab -e**
4. (Assuming nano editor) Use the arrow keys to navigate to the line with the disabled reboot command.
5. Uncomment this line by deleting the '#' symbol
6. Save the file by pressing this sequence of keys: CTRL+X, Y, ENTER
7. You can now safely shutdown or reboot the RPi

# Disable autorun
1. To run BlindVision fitness manually on reboot, you must first open the RPi either through desktop or SSH/VNC.
2. Open the terminal if you haven't already
3. Enter the following command: **crontab -e**
4. (Assuming nano editor) Use the arrow keys to navigate to the line with the enabled reboot command.
5. Comment out this line by adding the '#' symbol to the front
6. Save the file by pressing this sequence of keys: CTRL+X, Y, ENTER
7. You can now safely shutdown or reboot the RPi
