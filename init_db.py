import os
import pymysql
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

host = os.getenv('MYSQLHOST', '127.0.0.1')
port = int(os.getenv('MYSQLPORT', 3306))
user = os.getenv('MYSQLUSER', 'root')
password = os.getenv('MYSQLPASSWORD', '')

# We explicitly define the target DB name we WANT to create:
target_db = "northstar_db"

print(f"Connecting to MySQL server at {host}:{port}...")

try:
    # Connect to MySQL host WITHOUT specifying a database
    connection = pymysql.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        autocommit=True
    )

    with connection.cursor() as cursor:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{target_db}`;")
        print(f"✅ Database '{target_db}' successfully created/verified on Railway!")

    connection.close()
except Exception as e:
        print(f"❌ Failed to create database: {e}")