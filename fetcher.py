import sqlite3
from convokit import Corpus

# ---------------------------------------------------------------------------- #
#                                                                              #
# ---------------------------------------------------------------------------- #
# OP Posts                                                                     #
# ---------------------------------------------------------------------------- #
#                                                                              #
# ---------------------------------------------------------------------------- #
def get_op_posts(path_to_db):
    con = sqlite3.connect(path_to_db)
    cur = con.cursor()

    posts_cur = cur.execute("SELECT id FROM CMV WHERE id = root_id")
    posts_ids = cur.fetchall()

    return posts_ids

