import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database.connection import engine

try:
    connection = engine.connect()
    print("Database Connected Successfully")
    connection.close()
except Exception as e:
    print("Database Connection Failed")
    print(e)