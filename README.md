# Background


# System Design


# Server Setup

## Rasberry Pi Setup
e.g. Python packages, wifi setup, power saving config
### Install required softwares
1. Install Wand from http://docs.wand-py.org/
    ```` 
    sudo apt-get update
    sudo apt-get install libmagickwand-dev
    sudo pip install Wand
    
    sudo pip install dropbox
    ````
2. 

## Project Setup
, e.g. project folders, Crontab setup 

# Web Service in Use


# Script Workflow
1. Get file list in play order into file_list.txt
2. Download files into "download" folders
3. For each file in file_list with index i
	Get file from download folder
	If it's a image file, copy to "pictures" folder and rename it as "<i>_<filename>"
	If it's a pdf file, export it as images to "pictures" foder with name "<i>_<filename>_<page>"
	If it's video file, copy it to "videos" folder
4. Run Feh with slide show
5. Play video files
