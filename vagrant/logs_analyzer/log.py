#!/usr/bin/env python3

import psycopg2


# Outputs the most famous authors from most famous to least famous
def popular_authors():
    db = psycopg2.connect("dbname=news")
    query = "SELECT name, count(substr(log.path,10)) as views " \
            "FROM authors INNER JOIN articles " \
            "ON articles.author = authors.id " \
            "INNER JOIN log ON articles.slug = substr(log.path,10) " \
            "WHERE log.path != '/' GROUP BY name ORDER BY views DESC;"
    cursor = db.cursor()
    cursor.execute(query)
    posts = cursor.fetchall()
    db.close()
    print("Most famous author classification:")
    for author, number in posts:
        print(str(author) + "- - - -" + str(number) + " views")
    print('\n')


# Outputs the three most popular articles per page request
def popular_articles():
    db = psycopg2.connect("dbname=news")
    query = "SELECT title, count(substr(log.path,10)) as views " \
            "FROM articles INNER JOIN log " \
            "ON articles.slug = substr(log.path,10) " \
            "WHERE log.path != '/' GROUP BY title ORDER BY views DESC LIMIT 3;"
    cursor = db.cursor()
    cursor.execute(query)
    posts = cursor.fetchall()
    db.close()
    print("Top 3 most viewed articles:")
    for title, number in posts:
        print(str(title) + "- - - -" + str(number) + " views")
    print('\n')


# Outputs the days on which the error rate was above 1%
def errors():
    db = psycopg2.connect("dbname=news")
    query = "SELECT TO_CHAR(result.date_error, 'Mon DD, YYYY'), " \
            "result.percent_errors FROM result;"
    cursor = db.cursor()
    cursor.execute(query)
    posts = cursor.fetchall()
    db.close()
    print("Day in which the output rate was higher than 1%:")
    for date, percent in posts:
        print(str(date) + "- - - -" + str(percent) + "% errors")
    print('\n')


if __name__ == "__main__":
    popular_articles()
    popular_authors()
    errors()
