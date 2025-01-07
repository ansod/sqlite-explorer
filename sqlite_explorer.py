import os
import sqlite3 as sql
import argparse
import webbrowser
from threading import Timer
from typing import Any

from flask import Flask, render_template


app = Flask('SQLite explorer', template_folder=os.path.relpath('.'))


class Explorer:
    def __init__(self, db: str, cur: sql.Cursor):
        self.db = db
        self.cur = cur

    def get_tables(self) -> list[str]:
        self.cur.execute("SELECT name FROM sqlite_master WHERE type='table';")

        return [tab[0] for tab in self.cur.fetchall()]

    def get_table(self, table: str) -> list[dict[str, Any]]:
        self.cur.execute(f"SELECT * FROM {table}")

        return [dict(row) for row in self.cur.fetchall()]

    def start_flask(self):

        @app.route('/')
        def index():
            tables = self.get_tables()
            content = {}
            for table in tables:
                content[table] = self.get_table(table)

            return render_template('app.html', content=content)

        app.run(host='0.0.0.0', port=8080)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Description of your program')
    parser.add_argument("dbname", help='Name of your sqlite database file.')
    args = parser.parse_args()
    db = args.dbname

    if not os.path.isfile(db):
        print(f'Could not find database file named {db}')
        exit(1)

    conn = sql.connect(db, check_same_thread=False)
    conn.row_factory = sql.Row
    cur = conn.cursor()
    exp = Explorer(db, cur)
    Timer(0.8, lambda: webbrowser.open_new('http://127.0.0.1:8080')).start()
    exp.start_flask()
