#Wiki table scraper and SQL insertion

I made this Python 2.7 script to help a friend in SurreyCodes to scrape data from a wiki table and insert them in a SQl database.

## Problem to solve

From the wiki table "https://en.wikipedia.org/wiki/List_of_districts_of_Costa_Rica" we need to scrape the table "District of Costa Rica" of three column: Province, Canton and District and insert in a SQL database where the three tables are: Cantón, Distrito and Provincia.
In Distrito and Cantón there are one ID table that refer to: for Cantón to a Provincia ID and for Distrito to a Cantón ID.

## Difficulties

The table Cantón is not ascii characters but utf-8 characters that difference gave me a lot difficulties to find a solution, first I wrote on the top of the code the line:

-*- coding: utf-8 -*-

but was not enought for the python interpreter, I added  this line of code:

reload(sys)
sys.setdefaultencoding('utf-8')

to reload sys and encoding to prevent errors.

## Main-mariadb

I written this code on a OpenSuse Leap 42.3 because the first script written on LinuxMint 18.3 had some running problem and the mariadb server was hosted in OpenSuse 42.2 distro.

Packages required:

- Beautifulsoup
- mysql-connector

On Suse you can install the packages required with:

$ sudo zypper in -t package python-beautifulsoup
$ sudo zypper in -t package python-mysql-connector-python

## Main-mysql

I written this code first on my LinuxMint 18.3 with a MySQL installation.
