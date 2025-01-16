import sqlite3

class ConsoleMessages:
    MAIN_MENU = """
Choose search-type:
1. Search by keyword
2. Search by genre and year
3. Top 5 search queries
q. Exit
"""


class SqlQueries:
    SEARCH_BY_KEYWORD_Q = """
                SELECT ROW_NUMBER() OVER (ORDER BY title) AS num, 
                    title, 
                    description, 
                    release_year
                FROM film
                WHERE LOWER(title) LIKE %s OR LOWER(description) LIKE %s
                LIMIT %s OFFSET %s;
                                """
    SEARCH_BY_GENRE_YEAR_Q = """
                SELECT ROW_NUMBER() OVER (ORDER BY f.title) AS num,
                       f.title, f.release_year
                FROM film f
                JOIN film_category fc ON fc.film_id = f.film_id
                JOIN category c ON c.category_id = fc.category_id
                WHERE LOWER(c.name) LIKE %s AND f.release_year = %s
                LIMIT %s OFFSET %s;
                                """
    CREATE_TABLE_Q = """
                CREATE TABLE IF NOT EXISTS popular_queries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    query TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                    """
    INSERT_Q = """INSERT INTO popular_queries (query) VALUES (?);"""
    DISPLAY_TOP5_Q = """
                SELECT query, COUNT(query) as count FROM popular_queries
                GROUP BY query
                ORDER BY count DESC
                LIMIT 5;
                     """

class Exceptions:
    @staticmethod
    def handle(exception):
        """Обрабатывает исключения и выводит сообщение об ошибке."""
        if isinstance(exception, ValueError):
            print(f"Validation error: {exception}")
        elif isinstance(exception, sqlite3.OperationalError):
            print(f"Error executing SQL query: {exception}")
        elif isinstance(exception, sqlite3.ProgrammingError):
            print(f"Database operation error: {exception}")
        elif isinstance(exception, AttributeError):
            print(f"Error connecting to the database: {exception}")
        else:
            print(f"Unexpected error: {exception}")

