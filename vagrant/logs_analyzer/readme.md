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
`CREATE VIEW daily_errors as
SELECT to_char(log.time, 'FMMonth DD, YYYY') "day", count(log.status) as errors
FROM log WHERE status = '404 NOT FOUND'
GROUP BY 1 ORDER BY 1;
        
CREATE VIEW daily_requests as
SELECT to_char(log.time, 'FMMonth DD, YYYY') "day", count(log.status) as requests
FROM log GROUP BY 1 ORDER BY 1;
        
CREATE VIEW error_day as
SELECT daily_errors.day, concat(ROUND((100.0 * daily_errors.errors / daily_requests.requests), 2), '%') as percent_errors
FROM daily_errors, daily_requests
WHERE daily_errors.day = daily_requests.day AND (((100.0 * daily_errors.errors / daily_requests.requests)) > 1)
ORDER BY percent_errors desc;`

Query:
`SELECT * FROM error_day;`

Output:
`Day in which the output rate was higher than 1%:
July 17, 2016- - - -2.26% errors`