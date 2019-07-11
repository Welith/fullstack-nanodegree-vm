# "Database code" for the DB Forum.

import psycopg2, bleach

def get_posts():
  db = psycopg2.connect("dbname=forum")
  cursor = db.cursor()
  cursor.execute("SELECT content, time FROM posts order by time DESC;")
  posts = cursor.fetchall()
  db.close()
  return posts

def add_post(content):
  db = psycopg2.connect("dbname=forum")
  cursor = db.cursor()
  cursor.execute("INSERT INTO posts VALUES (%s)", (bleach.clean(content, strip=True),))
  db.commit()
  db.close()


