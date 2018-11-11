# Udacity_FSND_Project_One

### This is the Log Analysis Project from the Udacity Full Stack Web Developer Nanodegree Program
* The purpose of this application is to use Python to connect to a PostgreSQL database and return the results of three queries that answer the following questions:
    1. What are the most popular three articles of all time?
    1. Who are the most popular article authors of all time?
    1. On which days did more than 1% of requests lead to errors? 

## Software Requirements
* [Python 3.5.2 or higher]( https://www.python.org/downloads)
* [(PostgreSQL) 9.5.14](https://www.postgresql.org/download/)
* [psycopg2 2.7.6](http://initd.org/psycopg/download/)
* [Vagrant 2.2.0](https://www.vagrantup.com/downloads.html)
* [VirtualBox 5.2.2+](https://www.virtualbox.org/wiki/Downloads)

## Instructions For Installing Vagrant Virtual Machine

**These instructions, the Vagrant VM, and the SQL database are courtesy of [Udacity.com](https://www.udacity.com) and their [Full Stack Web Developer Nanodegree Program](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004)**

* **Install VirtualBox:**
VirtualBox is the software that actually runs the virtual machine. You do not need the extension pack or the SDK. You do not need to launch VirtualBox after installing it; Vagrant will do that.

* **Install Vagrant:**
Vagrant is the software that configures the VM and lets you share files between your host computer and the VM's filesystem. Install the version for your operating system.

Windows users: The Installer may ask you to grant network permissions to Vagrant or make a firewall exception. Be sure to allow this.

* **Install the Vagrant VM:**
There are a couple of different ways you can download the VM configuration.

You can download and unzip this file: [FSND-Virtual-Machine.zip](https://s3.amazonaws.com/video.udacity-data.com/topher/2018/April/5acfbfa3_fsnd-virtual-machine/fsnd-virtual-machine.zip) This will give you a directory called FSND-Virtual-Machine. It may be located inside your Downloads folder.

Alternately, you can use Github to fork and clone the repository [https://github.com/udacity/fullstack-nanodegree-vm](https://github.com/udacity/fullstack-nanodegree-vm).

Either way, you will end up with a new directory containing the VM files. Change to this directory in your terminal with cd. Inside, you will find another directory called vagrant. Change directory to the vagrant directory:

## Instructions for starting the Virtual Machine, connecting to the database, and running the Python file 

* **Start the virtual machine**
From your terminal, inside the vagrant subdirectory, run the command **vagrant up**. This will cause Vagrant to download the Linux operating system and install it. This may take quite a while (many minutes) depending on how fast your Internet connection is.

When vagrant up is finished running, you will get your shell prompt back. At this point, you can run **vagrant ssh** to log in to your newly installed Linux VM!

* **Download the SQL database**

Next, [download the data here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip). You will need to unzip this file after downloading it. The file inside is called newsdata.sql. Put this file into the vagrant directory, which is shared with your virtual machine.

To load the data, cd into the vagrant directory and use the command: 

```bash
psql -d news -f newsdata.sql.
```
After the database information finishes loading connect to the database with the following command:

```bash
psql -d news
```

* **Please execute all of the queries in the Create Views section below**

Once all of the Views have been created you can exit the database and run the Python file.

Run the Python file by executing the following command:

```bash
python3 newsdata_db.py
```

* It is possible that the psycopg2 library is not present in your current Python venv. If this is the case you will receive an error when running the Python file. If you receie an error referencing psycopg2, please run the following command within your venv directory to install psycopg2 **--this may require superuser privilages**

```bash
pip3 install psycopg2
```

## Create Views

* All of the views listed below under "Create Views" **MUST** be created in order for the Python queries to execute successfully

### View to List Author, Title, and Slug for Articles

```sql
CREATE VIEW article_summary AS
SELECT
authors.name AS "Article Author",
articles.title AS "Article Title",
articles.slug AS "Article Slug"
FROM articles
JOIN authors
ON articles.author = authors.id
ORDER BY authors.name;
```

### View to Seperate Slug from log.path
* Ex. /article/goats-eat-googles --> goats-eat-googles

```sql
CREATE VIEW slug_from_path AS
SELECT
articles.slug
FROM
articles
JOIN log ON substr(log.path, length('/article/')+1) = articles.slug;
```


### View of Number of Views per Date:

```sql
CREATE VIEW total_views_by_date AS
SELECT date(time) AS "Date Viewed", COUNT(*) AS "Number of Views"
FROM log
GROUP BY date(time)
ORDER BY date(time);
```

### View of Views per Slug

```sql
CREATE VIEW slug_and_count AS
SELECT slug AS "Article Slug", COUNT(*) AS "Article View Count"
FROM slug_from_path
GROUP BY slug
ORDER BY "Article View Count" DESC;
```

### View To Find and Count 404 Errors

```sql
CREATE VIEW not_found_error AS
SELECT date(time) AS "Date", COUNT(*) AS "404 Errors"
FROM log
WHERE status LIKE '%404%'
GROUP BY date(time)
ORDER BY date(time);
```


### View To Find Percent of 404 Errors That Occured

```sql
CREATE VIEW percent_error AS
SELECT
not_found_error."Date", (100.00*not_found_error."404 Errors"/total_views_by_date."Number of Views")
AS "Percent Error(%)"
FROM not_found_error
JOIN total_views_by_date
ON not_found_error."Date" = total_views_by_date."Date Viewed"
ORDER BY not_found_error."Date";
```

### View For Solution to Question 1: What are the most popular three articles of all time?

```sql
CREATE VIEW top_three_articles AS
SELECT
article_summary."Article Title" AS "Top Three Articles",
slug_and_count."Article View Count" AS "Number of Views"
FROM article_summary
JOIN slug_and_count
ON article_summary."Article Slug" = slug_and_count."Article Slug"
ORDER BY slug_and_count."Article View Count" DESC
LIMIT 3;
```

### View For Solution to Question 2: Who are the most popular article authors of all time?

```sql
CREATE VIEW top_authors AS
SELECT
article_summary."Article Author",
SUM(slug_and_count."Article View Count") AS "Total Views"
FROM article_summary
JOIN slug_and_count
ON article_summary."Article Slug" = slug_and_count."Article Slug"
GROUP BY article_summary."Article Author"
ORDER BY "Total Views" DESC;
```


