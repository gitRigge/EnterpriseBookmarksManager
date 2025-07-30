# Enterprise Bookmarks Manager

![Tests](https://github.com/gitRigge/EnterpriseBookmarksManager/actions/workflows/tests.yml/badge.svg)
![Coverage](https://raw.githubusercontent.com/gitRigge/EnterpriseBookmarksManager/main/coverage/coverage.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: Flake8](https://img.shields.io/badge/code%20style-flake8-000000.svg)](https://github.com/pycqa/flake8)

This app is able to convert Microsoft 365 Admin Center Enterprise Bookmarks CSV export to Excel and vice versa.

## Introduction

The Microsoft 365 Admin Center allows to define so called Enterprise Bookmarks in the section Search & Intelligence, Answers, see [Manage Bookmarks](https://learn.microsoft.com/en-us/microsoftsearch/manage-bookmarks). The GUI of the Admin Center is pretty crappy. As a result, I recommend to export all bookmarks and to edit the bookmarks in Excel. The Enterprise Bookmarks Manager helps to convert the CSV file into an Excel file and vice versa.

## Build

Just run the make file, wait until it ends and have a look at the release folder:

```makeExe.bat```

Or download the latest release from the [GitHub repo release folder](https://github.com/gitRigge/EnterpriseBookmarksManager/blob/main/release/enterprise_bookmarks_manager.zip)

## Run

Simply run enterprise_bookmarks_manager.exe. If no further argument has been provided, the Enterprise Bookmarks Manager looks for a suitable file and asks you whether to continue. In addition, you can run the Enterprise Bookmarks Manager with an argument.

### Interactive mode

Just run the app to use the interactive mode:

```enterprise_bookmarks_manager.exe```

In this mode, the app tries to detect a bookmark file in the current working directory. If it finds multiple files that fit, it suggests the latest one. In any case, it will ask you to confirm to continue.

### CLI mode

Or open a command line and call the app with an argument:

```enterprise_bookmarks_manager.exe -i Bookmarks_from_Admin_Center.csv```

This will result in the Excel file 'Bookmarks_from_Admin_Center.xlsx'

Or call the app like this:

```enterprise_bookmarks_manager.exe -i Bookmarks_to_Admin_Center.xlsx```

This will result in the CSV file 'Bookmarks_to_Admin_Center.csv' which you then can import in the Admin Center.

The app comes with a few more helpful options, see help:

```enterprise_bookmarks_manager.exe -h```

    
    usage: enterprise_bookmarks_manager.exe [-h] [-i INPUTFILE] [-c] [-v] [-d] [-s] [-l] [--version]

    Generates xlsx files to work with Excel or csv files to import in Admin Center.

    options:
    -h, --help            show this help message and exit
    -i, --inputfile INPUTFILE
                            Specify input file to read (Excel or CSV)
    -c, --countries       Show list of ISO country codes and exit
    -v, --variations      Show sample variations JSON and exit
    -d, --devices         Show list of devices and exit
    -s, --status          Show list of status and exit
    -l, --license         Show license information and exit
    --version             show program's version number and exit

    For more help, see: https://github.com/gitRigge/EnterpriseBookmarksManager

### Development

Run this command to install all requirements. I'd like to recommend to run it in a virtual environment:

`pip install -r requirements.txt`


Then run this command to clean and test everything:

`tox`
