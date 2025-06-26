# Overview

This piece of software is a typing speed/accuracy trainer. Using a SQL relational database, this trainer will present 
a user with a paragraph to type, and record data from each practice session, including how many words were mispelled and 
a user's words per minute. Data is stored from user to user, so multiple people can benefit at the same time. To start your training,
simply create a user, select practice on the main menu, and off you go! The menus are simple and self explanatory. You can view
a user's history from the main menu, which will inform you of past practice session, average words mispelled per session, and 
the user's personal record for fastest words per minute.

I wrote this software because I was interested in learning how to manage a SQL relational database. I chose a typing trainer
simply because it sounded like a fun thing I could do that sort of felt like a game in a compete with myself kind of way. 
It's not fancy by any means, but it has a simple kind of fun to it that helps you improve your typing ability at the same time.

# Relational Database

I'm using a SQL relational database to store two primary types of data, which is the paragraphs given to the user to type, 
and data about each user's practice sessions.

To begin, there will be one table that contains all paragraphs to be displayed. From there,
each time a new user is created, they will be given their own unique table in the database.
In this table will be stored data from each of that user's practice sessions.

# Development Environment

Typing trainer was made using vscode. It is built in Python using the sqlite3 library primarily. It also uses the timeit and random libraries. 

# Useful Websites

* [sqlite tutorial website](https://www.sqlitetutorial.net/sqlite-python/)
* [sqlite3 documentation](https://docs.python.org/3/library/sqlite3.html)

# Future Work

* Expanding paragraph pool. It is still quite small
* Error handling. There is currently no testing to see if a username entered exists, or for catching typos.
* Add additional practice modes, like maybe single words at a time instead of paragraphs. Like a flash round type of thing.
