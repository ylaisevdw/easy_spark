## Easy Spark application
The GUI is deployed as a containerized application with Docker.

### Required installations
1. Docker
Docker (desktop) should be installed on your pc, see https://www.docker.com/products/docker-desktop.

2. X Server
Your pc needs to have installed a X Server suite in order to display the GUI. This is by default installed at the Linux OS.

For Windows you can install: https://sourceforge.net/projects/vcxsrv/

For Mac OS you can install: https://www.xquartz.org/

### Add input files
At the moment, only some input files are available in the Docker application. You can manually add additional input files into the app/input_file folder

### Change IP address in start.sh
You should change the ip variable in the starh.sh file into your local IP address. In Windows, you can simply enter the ``` ipconfig ``` PowerShell command and obtain the IPv4 address of Wireless LAN adapter Wi-Fi.

### Run application
Run ``` $ docker compose up ```