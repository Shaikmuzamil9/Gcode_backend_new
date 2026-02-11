import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASS = os.getenv("DB_PASS", "")
DB_NAME = os.getenv("DB_NAME", "gcode_transmitter")

def get_db_connection():
    ports_to_try = []

    env_port = os.getenv("DB_PORT")
    if env_port and env_port.isdigit():
        ports_to_try.append(int(env_port))

    ports_to_try.extend([3306, 3307])
    ports_to_try = list(dict.fromkeys(ports_to_try))

    last_error = None

    for port in ports_to_try:
        try:
            conn = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASS,
                database=DB_NAME,
                port=port,
                charset="utf8mb4",
                autocommit=True,
                connection_timeout=5
            )
            return conn
        except Error as e:
            last_error = e

    raise Exception(f"DB Connection failed: {last_error}")
