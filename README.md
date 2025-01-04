# Pobierz

## Download scans from Archives

This little python program may be used to download a set of archive zip files.
This is the very first prototype and far not ready yet.


### Requirements:
In order to run this program you should have installed a python3 environment with these modules available:
* Pandas
* Regular Expressions (re)
* logging
* BeautifulSoup

## Installation:
Please make sure you have a proper python environment installed on your computer. 
The program has been testet using Windows 10 and a Ubuntu 24.04 environments:

#### Python on Linux:
Most Linux distributiuons already come with python3 preinstalled. 
Just refer to your distribution installation instruction on how to install python3 with pip.

#### Python on Windows:
If you do not yet have a Python environemnt installed please refer to these installation instructions for a Windows-System using
[Anaconda Installation](https://docs.anaconda.com/anaconda/install/windows/).


#### Program installation:
For instruction on how to use git see [GIT](https://git-scm.com/)

Get the latest source code from this repository by cloning into your workspace:
```sh
git clone https://github.com/Deichgeist/Pobierz.git
```
if you just need to update your existing repository to the latest version, apply:
```sh
git pull
```

If you just need a simple download with no capabilities to update the software, then simply download the actual package from this webpage.


#### Installing required pythpn modules and packages:

It is strongly recommended to create a virtual python environment inside the folder. This can be done in a bash like this:
````sh
python3 -m venv venv
````
than activate the virtual environment:
````sh
source venv/bin/activate
````

make sure you have the virtual environment activated, theninstall the required python packages:

```sh
pip install -r requirements.txt
```
You are almost done....  :thumbsup:

### Run the program

Find the Zespol-ID of the fond you'd like to download.
start the program and pass the ID as parameter:
```sh
python3 pobierzwarchiwach.py 111067
```

Have fun! :heart_eyes:
