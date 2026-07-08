import sqlite3


DATABASE_NAME = "history.db"


def connect_database():

    connection = sqlite3.connect(DATABASE_NAME)

    return connection


def create_table():

    connection = connect_database()

    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS browser_history(

        id INTEGER PRIMARY KEY,

        title TEXT,

        url TEXT,

        saved_time TEXT

    )
    """)

    connection.commit()

    connection.close()


def insert_history(history_id, title, url, saved_time):

    connection = connect_database()

    cursor = connection.cursor()

    cursor.execute("""
    INSERT OR IGNORE INTO browser_history
    VALUES(?,?,?,?)
    """, (
        history_id,
        title,
        url,
        saved_time
    ))

    connection.commit()

    connection.close()


def get_all_history():

    connection = connect_database()

    cursor = connection.cursor()

    cursor.execute("""
    SELECT
        id,
        title,
        url,
        saved_time
    FROM browser_history
    ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    connection.close()

    return rows


def total_records():

    connection = connect_database()

    cursor = connection.cursor()

    cursor.execute("""
    SELECT COUNT(*)
    FROM browser_history
    """)

    count = cursor.fetchone()[0]

    connection.close()

    return count


def search_history(keyword):

    connection = connect_database()

    cursor = connection.cursor()

    cursor.execute("""
    SELECT
        id,
        title,
        url,
        saved_time
    FROM browser_history
    WHERE
    title LIKE ?
    OR
    url LIKE ?
    ORDER BY id DESC
    """, (
        "%" + keyword + "%",
        "%" + keyword + "%"
    ))

    rows = cursor.fetchall()

    connection.close()

    return rows
import csv

def export_to_csv():

    connection = connect_database()

    cursor = connection.cursor()

    cursor.execute("""
    SELECT
        id,
        title,
        url,
        saved_time
    FROM browser_history
    ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    with open(
        "history_export.csv",
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "ID",
            "Title",
            "URL",
            "Saved Time"
        ])

        writer.writerows(rows)

    connection.close()

