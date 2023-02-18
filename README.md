# Enterprise Bookmarks Manager

![Tests](https://github.com/gitRigge/EnterpriseBookmarksManager/actions/workflows/tests.yml/badge.svg)
![Coverage](https://raw.githubusercontent.com/gitRigge/EnterpriseBookmarksManager/main/coverage/coverage.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

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

### CLI mode

Or open a command line and call the app with an argument:

```enterprise_bookmarks_manager.exe Bookmarks_from_Admin_Center.csv```

This will result in the Excel file 'Bookmarks_from_Admin_Center.xlsx'

Or call the app like this:

```enterprise_bookmarks_manager.exe Bookmarks_from_Admin_Center.xlsx```

This will result in the CSV file 'Bookmarks_from_Admin_Center.csv' which you then can import in the Admin Center.
