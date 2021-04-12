# Pobierz

## Download scans from Archives

This little python program may be used to download a set of archive zip files.
This is the very first prototype and far not ready yet.


### Requirements:
In order to run this program you should have installed a python3 environment with these modules available:
* Numpy and Pandas
* xlsxwriter
* Regular Expressions (re)
* multiprocessing
* logging
* BeautifulSoup
* and a http parser like lxml (required by BeautifulSoup)

## Installation:
Please make sure you habe a proper python environment installed on your computer. 
The program has been testet using Windows 10 and a Ubuntu 20.04 environments:

#### Python on Linux:
Most Linux distributiuons already come with python3 preinstalled. 
Just refer to your distribution installation instruction on how to install python3 with pip.

#### Python on Windows:
If you do not yet have a Python environemnt installed please refer to these installation instructions for a Windows-System using
[Anaconda Installation](https://docs.anaconda.com/anaconda/install/windows/).

#### Installing required modules:
just in case some of the required modules are still missing, apply:
```
pip install ......  (to be tested)
```

#### Program installation:
For instruction on how to use git see [GIT](https://git-scm.com/)

Get the latest source code from this repository by cloning into your workspace:
```
git clone https://github.com/Deichgeist/Pobierz.git
```
if you just need to update your existing repository to the latest version, apply:
```
git pull
```

If you just need a simple download with no capabilities to update the software, then simply download the actual package from this webpage.

### Run the program
Find the Zespol-ID of the fond you'd like to download.
start the program and pass the ID as parameter:
```
python pobierzwarchiwach.py 111067
```

Have fun!
