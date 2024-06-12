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

def get_success_posts_reply_to_text(path_to_db) -> list:
    con = sqlite3.connect(path_to_db)
    cur = con.cursor()

    pairs = []
    ids = get_ids("SELECT id, reply_to, root_id FROM CMV WHERE success = 1, root_id=reply_to", path_to_db)

    for id in ids:
        ut_id, reply_to, root_id = id

        ut_cur = cur.execute(f"SELECT text FROM CMV WHERE id = '{ut_id}'")
        ut_text = ut_cur.fetchone()[0]

        reply_to_cur = cur.execute(f"SELECT text FROM CMV WHERE id = '{reply_to}'")
        reply_to_text = reply_to_cur.fetchone()[0]

        root_cur = cur.execute(f"SELECT text FROM CMV WHERE id = '{root_id}'")
        root_text = root_cur.fetchone()[0]

        pairs.append((ut_text, reply_to_text, root_text))

    return pairs

def get_unsuccess_posts(path_to_db) -> list:
    return get_ids("SELECT id, root_id FROM CMV WHERE success = 0", path_to_db)

