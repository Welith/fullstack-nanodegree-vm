# Udacity SQL loger task
A simple SQL logger, which is used to answer three specific questions.

## Table of content
* Usage
* Three most viewed articles SQL query
* Most read author based on article viewing SQL query
* Day with more than 1% error rate SQL query

## Usage
* Install VBox and Vagrant
* Start the virtual machine with `vagrant up`.
* After the install is complete, run `vagrant ssh` to connect to the VM.
* `cd /vagrant` to go into the project directory and look around.
* Download the project sql file.
* Run `psql -d news -f newsdata.sql` to load the downloaded file into the DB that is already set-up for you.
* Run `psql -d news` to log into the project DB

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
Views:
`CREATE VIEW errors as
SELECT CAST(log.time as DATE) AS date_error, COUNT(log.status) as errors
FROM log WHERE status LIKE '%404%' GROUP BY date_error;
        
CREATE VIEW requests as
SELECT CAST(log.time as DATE) AS date_request, COUNT(log.status) as requests
FROM log GROUP BY date_request;
        
CREATE VIEW result as
SELECT errors.date_error, ROUND((100.0 * errors.errors / requests.requests), 3) as percent_errors
FROM errors INNER JOIN requests ON errors.date_error = requests.date_request
WHERE (((100.0 * errors.errors / requests.requests)) > 1)
ORDER BY percent_errors DESC;`

Query:
`SELECT TO_CHAR(result.date_error, 'Mon DD, YYYY'), result.percent_errors FROM result;`

Output:
`Day in which the output rate was higher than 1%:
July 17, 2016- - - -2.263% errors`