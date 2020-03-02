from cube_2x2x2 import Cube
from BFS import BFS
import numpy as np
import sqlite3
import time


def create_db(path):
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS States(ID VARCHAR, value INT)")
    conn.commit()
    conn.close()


def update_db(path, table):
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    cur.executemany("INSERT INTO States(ID, Value) VALUES (?, ?)", table.items())
    conn.commit()
    conn.close()


def get_state(cube):
    state = ""
    for id, face in cube.faces.items():
        for color in face:
            state += color
    return state


if __name__ == "__main__":

    # generate all possible states of the cube
    data = BFS()

    # store data in database
    create_db("pattern.db")
    update_db("pattern.db", data)
