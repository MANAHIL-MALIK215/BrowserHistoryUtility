from pathlib import Path
import shutil
import sqlite3
import time
from datetime import datetime
import psutil
import os
import logging

import database

# -------------------------------------
# Logging Configuration
# -------------------------------------
logging.basicConfig(
    filename="logs.log",
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%d-%m-%Y %H:%M:%S"
)

logger = logging.getLogger(__name__)

logger.info("Browser History Utility Started")

# -------------------------------------
# Create Table
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

logger.info("Monitoring Started")

# -------------------------------------
# Batch Size
# -------------------------------------
BATCH_SIZE = 500

while True:

    start_time = time.perf_counter()

    total_records = 0
    batch_count = 0
    status = "Success"

    try:

        if not history_path.exists():

            logger.critical("Edge History File Not Found")

            print("History file not found.")

            break

        # Copy Database

        temp_history = home / "TempHistory"

        shutil.copy2(history_path, temp_history)

        logger.info("History database copied successfully")

        edge_connection = sqlite3.connect(temp_history)

        edge_cursor = edge_connection.cursor()

        logger.info("Connected to Edge SQLite Database")

        # Read last processed ID

        try:

            with open("last_id.txt", "r") as file:

                last_id = int(file.read())

            logger.debug(f"Last Processed ID : {last_id}")

        except:

            logger.warning("last_id.txt not found. Starting from ID 0")

            last_id = 0

        edge_cursor.execute("""

        SELECT
            id,
            title,
            url

        FROM urls

        WHERE id > ?

        ORDER BY id

        """, (last_id,))

        newest_id = last_id

        while True:

            rows = edge_cursor.fetchmany(BATCH_SIZE)

            if not rows:

                break

            batch_count += 1

            logger.info(
                f"Processing Batch {batch_count} ({len(rows)} Records)"
            )

            print(f"\nProcessing Batch {batch_count} ({len(rows)} Records)\n")
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
                total_records += 1

                logger.debug(
                    f"Saved Record | ID={history_id} | Title={title}"
                )

                print("Saved :", title)

        # -------------------------------------
        # Save Last ID
        # -------------------------------------
        if newest_id != last_id:

            with open("last_id.txt", "w") as file:

                file.write(str(newest_id))

            logger.info(f"Updated last_id.txt to {newest_id}")

        else:

            status = "No New History"

            logger.info("No New History Found.")

            print("No New History Found.")

        edge_connection.close()

        logger.info("SQLite Connection Closed")

        # -------------------------------------
        # Delete Temp File
        # -------------------------------------
        if temp_history.exists():

            temp_history.unlink()

            logger.info("Temporary History File Deleted")

    except Exception as e:

        status = "Error"

        logger.error(f"Exception Occurred : {e}")

        print("Error :", e)

    # -------------------------------------
    # Performance Metrics
    # -------------------------------------
    end_time = time.perf_counter()

    execution_time = end_time - start_time

    process = psutil.Process(os.getpid())

    memory_usage = process.memory_info().rss / (1024 * 1024)

    print("\n" + "=" * 40)
    print("PERFORMANCE METRICS")
    print("=" * 40)
    print(f"Status            : {status}")
    print(f"Records Processed : {total_records}")
    print(f"Batch Size        : {BATCH_SIZE}")
    print(f"Batches Processed : {batch_count}")
    print(f"Execution Time    : {execution_time:.3f} seconds")
    print(f"Memory Usage      : {memory_usage:.2f} MB")
    print("=" * 40)

    logger.info(
        f"Cycle Completed | "
        f"Status={status} | "
        f"Records={total_records} | "
        f"Batches={batch_count} | "
        f"Execution={execution_time:.3f}s | "
        f"Memory={memory_usage:.2f}MB"
    )

    print("\nChecking again in 5 seconds...")
    print("-" * 60)

    time.sleep(5)