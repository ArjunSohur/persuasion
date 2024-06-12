import sqlite3
from convokit import Corpus

# ---------------------------------------------------------------------------- #
#                                                                              #
# ---------------------------------------------------------------------------- #
# Getting ids from command function                                            #
# ---------------------------------------------------------------------------- #
#                                                                              #
# ---------------------------------------------------------------------------- #
def get_ids(command: str, path_to_db: str) -> list:
    con = sqlite3.connect(path_to_db)
    cur = con.cursor()

    posts_cur = cur.execute(command)
    posts_ids = posts_cur.fetchall()

    return posts_ids

# ---------------------------------------------------------------------------- #
#                                                                              #
# ---------------------------------------------------------------------------- #
# get ids commands                                                             #
# ---------------------------------------------------------------------------- #
#                                                                              #
# ---------------------------------------------------------------------------- #
def get_op_posts(path_to_db: str) -> list:
    return get_ids("SELECT id FROM CMV WHERE id = root_id", path_to_db)

def get_success_posts(path_to_db) -> list:
    return get_ids("SELECT id, root_id FROM CMV WHERE success = 1", path_to_db)

def get_success_posts_reply_to(path_to_db) -> list:
    return get_ids("SELECT reply_to, root_id FROM CMV WHERE success = 1", path_to_db)

def get_unsuccess_posts(path_to_db) -> list:
    return get_ids("SELECT id, root_id FROM CMV WHERE success = 0", path_to_db)

