# Udacity SQL loger task
A simple SQL logger, which is used to answer three specific questions.
This project was done as my first task in completing the Full-stack web developer nano-degree.

## Table of content
* Overview
* Requirements
* How to run the project?
* Three most viewed articles SQL query
* Most read author based on article viewing SQL query
* Day with more than 1% error rate SQL query

## Overview
This task aims to test the students SQL knowledge by building an SQL database with 
predefined information and then running queries on it, in order to answer three separate questions:
* Which are the three most viewed articles?
* Which are the most popular authors based on article views?
* Which days have more than 1% error rate in page responses?

## Requirements
* [Python3](https://www.python.org/downloads/release/python-374/)
* [Vagrant](https://www.vagrantup.com/) - Builds the virtual environment
* [VirtualBox](https://www.virtualbox.org/) - VM virtualization
* [Git](https://git-scm.com/) - Version control

## How to run the project?
1. Install the latest version of Python from the [link](https://www.python.org/downloads/release/python-374/).
2. Download and install [VirtualBox](https://www.virtualbox.org/) and [Vagrant](https://www.vagrantup.com/).
3. Download Udacity's pre-configured [Vagrant file](https://d17h27t6h515a5.cloudfront.net/topher/2017/August/59822701_fsnd-virtual-machine/fsnd-virtual-machine.zip).
4. Clone this [repo](https://github.com/udacity/fullstack-nanodegree-vm).
5. Download this [DB file](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip).
6. After cloning the repo, navigate your terminal to the Udacity folder and type `cd /vagrant`.
7. Initialize the virtual machine with `vagrant up`.
8. After the install is complete, run `vagrant ssh` to connect to the VM. Your bash should now be under vagrant.
9. `cd /vagrant` to go into the project directory and look around.
10. Unpack the DB downloaded in step 5 into this folder.
11. Run `psql -d news -f newsdata.sql` to load the downloaded file into the DB that is already set-up for you.
12. Run `psql -d news` to log into the project DB.
13. In order to run the query for the third question, you must first run the views in the Day with more than 1% error rate SQL query section.
14. Use the `python log.py` command in the vagrant terminal to run the script.

## Three most viewed articles SQL query
Query:
`SELECT title, count(substr(log.path,10)) as views
FROM articles INNER JOIN log ON articles.slug = substr(log.path,10)
WHERE log.path != '/' GROUP BY title ORDER BY views DESC LIMIT 3;`

Output:
`Top 3 most viewed articles:
Candidate is jerk, alleges rival- - - -338647 views
Bears love berries, alleges bear- - - -253801 views
Bad things gone, say good people- - - -170098 views`

## Most read author based on article viewing SQL query
Query:
`SELECT name, count(substr(log.path,10)) as views
FROM authors INNER JOIN articles ON articles.author = authors.id
INNER JOIN log ON articles.slug = substr(log.path,10)
WHERE log.path != '/' GROUP BY name ORDER BY views DESC;`

Output:
`Most famous author classification:
Ursula La Multa- - - -507594 views
Rudolf von Treppenwitz- - - -423457 views
Anonymous Contributor- - - -170098 views
Markoff Chaney- - - -84557 views`

## Day with more than 1% error rate SQL query
The following views were used to answer this questions:

`CREATE VIEW errors as
SELECT CAST(log.time as DATE) AS date_error, COUNT(log.status) as errors
FROM log WHERE status LIKE '%404%' GROUP BY date_error;`
        
`CREATE VIEW requests as
SELECT CAST(log.time as DATE) AS date_request, COUNT(log.status) as requests
FROM log GROUP BY date_request;`
        
`CREATE VIEW result as
SELECT errors.date_error, ROUND((100.0 * errors.errors / requests.requests), 3) as percent_errors
FROM errors INNER JOIN requests ON errors.date_error = requests.date_request
WHERE (((100.0 * errors.errors / requests.requests)) > 1)
ORDER BY percent_errors DESC;`

Query:
`SELECT TO_CHAR(result.date_error, 'Mon DD, YYYY'), result.percent_errors FROM result;`

Output:
`Day in which the output rate was higher than 1%:
July 17, 2016- - - -2.263% errors`