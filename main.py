import os
from constant import *
import mysql.connector
import sqlite3
from tabulate import tabulate
import re
import datetime
import dotenv
from pathlib import Path


class DatabaseReader:
    """Класс для работы с MySQL базой данных на чтение."""
    def __init__(self, host, user, password, database):
        self.conn = self.create_connection(host, user, password, database)

    def create_connection(self, host, user, password, database):
        try:
            conn = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database,
                use_unicode=True,
                charset='utf8')
            print("Connection successful.")
            return conn

        except Exception as e:
            Exceptions.handle(e)

    def search_by_keyword(self, keyword, page=1, per_page=10):
        """Ищет фильмы по ключевому слову в названии или описании с нумерацией."""
        try:
            if not keyword or len(keyword) < 2:
                raise ValueError("Keyword is too short.")

            if page < 1 or per_page < 1:
                raise ValueError("Page number and results per page should be greater than zero.")

            offset = (page - 1) * per_page
            cursor = self.conn.cursor()

            query = SqlQueries.SEARCH_BY_KEYWORD_Q
            cursor.execute(query, (f'%{keyword.lower()}%', f'%{keyword.lower()}%', per_page, offset))
            return cursor.fetchall()

        except Exception as e:
            Exceptions.handle(e)

    def search_by_genre_year(self, genre, year, page=1, per_page=10):
        """Ищет фильмы по жанру и году выпуска."""
        try:
            if not genre or not year:
                print("Error: No genre or year specified.")
                return None

            offset = (page - 1) * per_page
            cursor = self.conn.cursor()

            query = SqlQueries.SEARCH_BY_GENRE_YEAR_Q
            cursor.execute(query, (f'%{genre.lower()}%', year, per_page, offset))
            return cursor.fetchall()

        except Exception as e:
            Exceptions.handle(e)

    def close_connection(self):
        if self.conn:
            self.conn.close()
            print("Connection closed.")


class DatabaseEdit: #corrected
    """Класс для управления SQLite базой данных редактирования."""
    def __init__(self):
        self.conn = sqlite3.connect('sqlite_edit.db')
        self.create_table()

    def create_table(self):
        """Создает таблицу популярных запросов, если её нет."""
        query = SqlQueries.CREATE_TABLE_Q
        self.conn.execute(query)
        self.conn.commit()

    def insert_query(self, query_text):
        """Добавляет запрос в таблицу популярных запросов."""
        query = SqlQueries.INSERT_Q
        self.conn.execute(query, (query_text,))
        self.conn.commit()

    def display_top5(self):
        """Возвращает 5 самых популярных запросов."""
        cursor = self.conn.cursor()
        query = SqlQueries.DISPLAY_TOP5_Q
        cursor.execute(query, )
        return cursor.fetchall()

    def close_connection(self):
        if self.conn:
            self.conn.close()


class Application:
    """Класс для взаимодействия с пользователем."""
    def __init__(self, db_reader, db_edit):
        self.db_reader = db_reader
        self.db_edit = db_edit

    def display_results(self, results, page=1):
        """Отображает результаты в виде таблицы с учетом пагинации."""
        headers = ["#", "Title", "Description", "Year"]
        if not results:
            print("No results.")
            return False

        print(f"\nPage {page}")
        print(tabulate(results, headers=headers, tablefmt="grid"))
        return True

    def display_popular_queries(self, results, page):
        """Отображает самые популярные поисковые запросы в виде таблицы с учетом пагинации."""
        headers = ["Popular queries", "Count"]

        if not results:
            print("No results.")
            return False

        print(f"\nPage {page}")
        print(tabulate(results, headers=headers, tablefmt="grid"))
        return True

    def get_valid_keyword(self):
        """Запрашивает ключевое слово и проверяет его корректность."""
        symbols = ".^$*&+?{}%[]|()"
        while True:
            keyword = input("Enter a keyword or 'q' to exit: ").strip()
            if keyword.lower() == 'q':
                return None
            if not keyword or len(keyword) < 2:
                print("Error: Keyword is too short.")
                continue
            if any(char in symbols for char in keyword):
                print("Error: Invalid characters.")
                continue
            if all(char.isalpha() or char.isdigit() for char in keyword):
                return keyword

    def get_valid_genre_year(self):
        """Запрашивает жанр и год, проверяет их корректность."""
        while True:
            user_input = input("Enter genre and year separated by a space or 'q' to quit: ").strip()
            if user_input.lower() == 'q':
                return None, None

            parts = user_input.split(' ')
            if len(parts) != 2:
                print("Error: Enter genre and year separated by a space.")
                continue

            genre, year = parts
            if parts[0].isdigit():
                print("Genre must be alphabetic.")
                continue
            if not re.match("^[a-zA-Z]+$", genre):
                print("Error: Genre can only contain letters.")
                continue
            current_year = datetime.datetime.now().year
            if not year.isdigit() or not (1900 <= int(year) <= current_year):
                print("Error: Incorrect year. Choose any from 1900 until", current_year)
                continue

            return genre, year

    def pagination_loop(self):
        """Обрабатывает ввод пользователя для перехода по страницам или выхода."""
        while True:
            next_action = input("Enter 'n' for next or 'q' for exit: ").strip().lower()
            if next_action == 'n':
                return True
            elif next_action == 'q':
                print("Exit.")
                return False
            else:
                print("Invalid input. Enter 'n' or 'q'.")

    def search_and_paginate(self, search_type: str):
        """Обрабатывает ввод пользователя для поиска или вывода топа поисков."""
        page = 1
        per_page = 10

        if search_type == '1':
            keyword = self.get_valid_keyword()
            if keyword is None:
                return
            query_params = keyword
        elif search_type == '2':
            genre, year = self.get_valid_genre_year()
            if genre is None or year is None:
                return
            query_params = (genre, year)
        elif search_type == '3':
            results = self.db_edit.display_top5()
            if not results or not self.display_popular_queries(results, page):
                print("No results found.")
            return
        else:
            return

        query_text = query_params if isinstance(query_params, str) else f"{query_params[0]} {query_params[1]}"
        self.db_edit.insert_query(query_text)

        while True:
            if search_type == '1':
                results = self.db_reader.search_by_keyword(query_params, page, per_page)
            else:  # search_type == '2'
                results = self.db_reader.search_by_genre_year(query_params[0], query_params[1], page, per_page)

            if not results or not self.display_results(results, page):
                print("Nothing to display.")
                break

            if not self.pagination_loop():
                break
            page += 1

    def start(self):
        """Запускает пользовательский выбор."""
        while True:
            print(ConsoleMessages.MAIN_MENU)

            choice = input("Enter 1, 2, 3 or 'q' to quit: ").strip().lower()
            if choice == 'q':
                break
            self.search_and_paginate(choice)

        self.db_reader.close_connection()
        self.db_edit.close_connection()


if __name__ == "__main__":
    dotenv.load_dotenv(Path('.env'))
    dbconfig = {'host': os.environ.get('host'),
                'user': os.environ.get('user'),
                'password': os.environ.get('password'),
                'database': 'sakila'}
    
    db_reader = DatabaseReader(**dbconfig)
    db_edit = DatabaseEdit()
    app = Application(db_reader, db_edit)
    app.start()
