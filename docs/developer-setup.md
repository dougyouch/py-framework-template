# Developer Setup Guide

Explains how to setup your local computer for development.

## Required software

* python3
  - with package venv
* AWS CLI

On a Mac

```
brew install python3 awscli
pip3 install venv
```

## Create env Folder

Create a folder to add project specific modules.

```
python3 -m venv env
```

## Working with VENV

VENV creates an **env** folder inside the project.  This is where the projects python packages are installed.

To use this environment you need to activate it.

```
source env/bin/activate
```

To deactivate the environment

```
deactivate
```

## Installing project packages

```
pip install -r requirements.txt
``

## Updating/Adding packages

Use __pip__ command to manage the packages of the project.  Afterwards generate a new requirements.txt file using:

```
pip freeze > requirements.txt
```

This will ensure all developers are using the same package versions.
