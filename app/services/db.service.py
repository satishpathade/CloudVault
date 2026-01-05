# app/services/db_service.py

import pymysql
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

def save_file_metadata(filename: str, object_key: str) -> None:
    connection = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        connect_timeout=5
    )

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO file_metadata (original_filename, s3_object_key)
                VALUES (%s, %s)
                """,
                (filename, object_key)
            )
        connection.commit()
    finally:
        connection.close()
