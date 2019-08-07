First install pip for Python2. Download the get-pip.py file from https://bootstrap.pypa.io/get-pip.py
$ cd <download location>
$ sudo -H python ./get-pip.py

Installing pip also installs Python3
To run Python3
$ python3

Install pip3 by just executing the same file as in the step above, but this time using Python3
$ sudo -H python3 ./get-pip.py

To install virtualenv via pip
$ sudo -H pip3 install virtualenv

{If you want to use virtualenv as is, read below, else skip to the next pair of braces}

Note that virtualenv installs to the python3 directory. For me it's:
$ /usr/local/share/python3/virtualenv

Create a virtualenvs directory to store all virtual environments
$ mkdir somewhere/virtualenvs

Make a new virtual environment with no packages
$ virtualenv somewhere/virtualenvs/<project-name> --no-site-packages

To use the virtual environment
$ cd somewhere/virtualenvs/<project-name>/bin
$ source activate

You are now using the virtual environment for <project-name>. To stop:
$ deactivate

{Continue installation}

To install virtualenvwrapper
$ sudo -H pip3 install virtualenvwrapper

Use the following command to find the location of Python3 on your system
$ which python3

Add the following lines to ~/.bashrc (or your own shell's initialisation file)
> VIRTUALENVWRAPPER_PYTHON='<Python3 location>'
> source /usr/local/bin/virtualenvwrapper.sh
> export WORKON_HOME=$HOME/.virtualenvs

Run the following commands
$ mkdir ~/.virtualenvs
$ source ~/.bashrc

All the virtual environments created using virtualenvwrapper will now be stored in ./virtualenvs

To create new Python3 virtual environment
$ mkvirtualenv <project name>

To create new Python2 virtual environment
$ mkvirtualenv --python=python2 <project name>

The virtualenv will automatically activate after creation

Install packages local to the python3 virtualenv (and not global to the system) using
$ pip3 install <package-name>

Install packages local to the python2 virtualenv (and not global to the system) using
$ pip install <package-name>

To exit the virtualenv
$ deactivate


# pip3 install mysqlclient