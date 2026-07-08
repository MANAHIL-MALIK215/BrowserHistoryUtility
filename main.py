from pathlib import Path
import shutil
import sqlite3
import time
from datetime import datetime

import database

# -------------------------------------
# Create Table (Only Once)
# -------------------------------------
database.create_table()

# -------------------------------------
# User Home Folder
# -------------------------------------
home = Path.home()

# -------------------------------------
# Edge History Location
# -------------------------------------
history_path = (
    home
    / "AppData"
    / "Local"
    / "Microsoft"
    / "Edge"
    / "User Data"
    / "Default"
    / "History"
)

print("=" * 60)
print("EDGE HISTORY MONITOR")
print("=" * 60)

while True:

    try:

        # -------------------------------------
        # Check History File
        # -------------------------------------
        if not history_path.exists():

            print("History file not found.")
            break

        # -------------------------------------
        # Copy Database
        # -------------------------------------
        temp_history = home / "TempHistory"

        shutil.copy2(history_path, temp_history)

        # -------------------------------------
        # Connect Edge Database
        # -------------------------------------
        edge_connection = sqlite3.connect(temp_history)

        edge_cursor = edge_connection.cursor()

        # -------------------------------------
        # Read Last Processed ID
        # -------------------------------------
        try:

            with open("last_id.txt", "r") as file:

                last_id = int(file.read())

        except:

            last_id = 0

        # -------------------------------------
        # Read Only New Records
        # -------------------------------------
        edge_cursor.execute("""

        SELECT
            id,
            title,
            url

        FROM urls

        WHERE id > ?

        ORDER BY id

        """, (last_id,))

        rows = edge_cursor.fetchall()

        if rows:

            newest_id = last_id

            print(f"\nFound {len(rows)} New Record(s)\n")

            for row in rows:

                history_id = row[0]
                title = row[1]
                url = row[2]

                current_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

                database.insert_history(
                    history_id,
                    title,
                    url,
                    current_time
                )

                newest_id = history_id

                print("Saved :", title)

            with open("last_id.txt", "w") as file:

                file.write(str(newest_id))

        else:

            print("No New History Found.")

        edge_connection.close()

    except Exception as e:

        print("Error :", e)

    print("\nChecking again in 5 seconds...")
    print("-" * 60)

    time.sleep(5)