# MyProject 🚀
"""Movie Data Collection Project"""
This mini-project focuses on searching for movies and integrating the collected data into a database. It involves: Movie Search: Develop a mechanism to search for movies based on various criteria (title, genre and year). Data Collection: Extract relevant information from the search results and extract top 5 most popular search data. Database Integration: Store the collected movie data in a structured database for efficient organization and retrieval. This project can be a valuable tool for building a movie database for personal use or further analysis.

## Installation
```bash
git clone https://github.com/andarie1/Movie-Data-Collection-Project.git
cd repo
pip install -r requirements.txt (includes important libs for more tools).
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Python libraries: mysql.connector, tabulate, re, datetime, dotenv, pathlib, sys, os.
Database installation: sqlite3.
constant.py will include db-requests, exceptions and a long-read for users choice. 
Database credentials inside .env file and included in .gitignore by classics. 
Nothing much... Very simple project to deploy:)
```

### Features
- 🗄️ **SQL Database** for reading movies.  
- 🛢️ **SQLite3 Database** for collecting users' popular search queries.  
- 📊 **Table Visualization** for displaying data.  
- 🔎🎬 **Search movies** by keyword or genre + release year.  
- 🏆 **Request top 5** popular search queries.

#### How to use:
Simply choose one of the following options of the "main-menu":
1. Search by keyword (one word only)
2. Search by genre and year (genre and year separated by a space)
3. Top 5 search queries (to check out top 5 popular searches and their count)
q. Exit (magic way to exit quickly like a ninja)

##### Scenarios to test:
-Should you fail to connect to Database Reader, application will be discontinued.
-Valid connection will give you 4 options on your choice. Invalid choice takes you back to the main-menu.
-Should you choose more than one keyword, input will be continued until a valid input.
-Choice for genre and year strictly in this sequence and divided by one space only.
Year must be between 1900 and current year only or error will appear.
Should you choose year in front of genre, error will appear. 
-Pagination choice is only between 'n' for next and 'q' to exit. Invalid input will cause an error and continue.

###### Additional info
Documentation:

A README file is provided, detailing:
-The purpose of the project.
-Instructions for setting up the database.
-A list of available application commands.
-Example usage scenarios.

Code Quality:

Follows PEP 8 coding standards.
The code is easy to read, understand, and maintain.

Testing:

All application commands are thoroughly tested.
Proper handling of cases where search results are empty etc.

Enhancements:

Additional filtering options may be added in the future (e.g., filtering movies by rating).



