## Easy Spark application
The GUI is deployed as a containerized application with Docker.

### Required installations
1. Docker\
Docker (desktop) should be installed on your pc, see https://www.docker.com/products/docker-desktop.

2. X Server\
Your pc needs to have installed a X Server suite in order to display the GUI. This is by default installed with Linux OS. \
For Windows you can install: https://sourceforge.net/projects/vcxsrv/, see https://www.youtube.com/watch?v=4SZXbl9KVsw (until 1:30) for installation details  \
For Mac OS you can install: https://www.xquartz.org/

### Add input files
At the moment, only some input files are available in the Docker application. You can manually add additional input files into the app/input_file folder

### Run application
Run ``` docker compose up ``` in the root folder of this application.