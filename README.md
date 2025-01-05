# Pobierz

## Download scans from Archives

This little python program can be used to download a set of archive zip files.
This is the very first prototype and far from finished.

![logo](logo.png)

### Requirements:
In order to run this program you should have a python3 environment installed with these modules available:
* Pandas
* logging
* BeautifulSoup

## Installation:
Please make sure you have a proper python environment installed on your computer. 
The program has been testet on Windows 10 and Ubuntu 24.04 environments:

#### Python on Linux:
Most Linux distributions already come with python3 pre-installed. 
Just refer to your distributions installation instructions on how to install python3 using pip.

#### Python on Windows:
If you do not already have a Python environment installed, see these installation instructions for a Windows system using
[Anaconda Installation](https://docs.anaconda.com/anaconda/install/windows/).


#### Program installation:
For instructions on how to use git see [GIT](https://git-scm.com/)

Get the latest source code from this repository by cloning into your workspace:
```sh
git clone https://github.com/Deichgeist/Pobierz.git
```
if you just want to update your existing repository to the latest version, apply:
```sh
git pull
```

If you just need a simple download with no capabilities to update the software, then just download the actual package from this website.


#### Installing required pythpn modules and packages:

It is strongly recommended that you create a virtual python environment within the folder. This can be done in a bash like this:
````sh
python3 -m venv venv
````
Then enable the virtual environment:
````sh
source venv/bin/activate
````

Make sure you have the virtual environment activated, then install the required Python packages:

```sh
pip install -r requirements.txt
```
You are almost done....  :thumbsup:

### Running the program

Find the Zespol-ID of the fond you'd like to download.
Run the program and pass the ID as parameter:
```sh
python3 pobierzwarchiwach.py 111067
```

Have fun with it! :heart_eyes:
