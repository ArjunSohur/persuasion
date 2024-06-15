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
    ids = get_ids("SELECT id, root_id FROM CMV WHERE success = 1 AND root_id=reply_to", path_to_db)

    for id in ids:
        ut_id, root_id = id

        ut_cur = cur.execute(f"SELECT text FROM CMV WHERE id = '{ut_id}'")
        ut_text = ut_cur.fetchone()[0]

        root_cur = cur.execute(f"SELECT text FROM CMV WHERE id = '{root_id}'")
        root_text = root_cur.fetchone()[0]

        pairs.append((ut_text, root_text))

    return pairs

def get_unsuccess_posts(path_to_db) -> list:
    return get_ids("SELECT id, root_id FROM CMV WHERE success = 0", path_to_db)

# ---------------------------------------------------------------------------- #
#                                                                              #
# ---------------------------------------------------------------------------- #
# get win/lose pairs                                                           #
# ---------------------------------------------------------------------------- #
#                                                                              #
# ---------------------------------------------------------------------------- #
"""
for some post, get the post(s) that changed the poster's mind as well as all of
the ones that didn't in a dictionary 

{post: ([winning posts], [losing posts])}
"""
def get_wl_pairs(path_to_db: str, n:int = 5) -> dict:
    con = sqlite3.connect(path_to_db)
    cur = con.cursor()

    pairs = {}
    ids = get_ids("SELECT id, root_id FROM CMV WHERE id = root_id", path_to_db)
    ids = ids[:n]

    for id in ids:
        post_id, root_id = id

        post_cur = cur.execute(f"SELECT text FROM CMV WHERE id = '{post_id}'")
        post_text = post_cur.fetchone()[0]

        win_cur = cur.execute(f"SELECT id FROM CMV WHERE root_id = '{post_id}' AND success = 1")
        win_ids = win_cur.fetchall()

        lose_cur = cur.execute(f"SELECT id FROM CMV WHERE root_id = '{post_id}' AND success = 0")
        lose_ids = lose_cur.fetchall()

        win_posts = []
        for win_id in win_ids:
            win_id = win_id[0]
            win_cur = cur.execute(f"SELECT text FROM CMV WHERE id = '{win_id}'")
            win_text = win_cur.fetchone()[0]
            win_posts.append(win_text)

        lose_posts = []
        for lose_id in lose_ids:
            lose_id = lose_id[0]
            lose_cur = cur.execute(f"SELECT text FROM CMV WHERE id = '{lose_id}'")
            lose_text = lose_cur.fetchone()[0]
            lose_posts.append(lose_text)

        if win_posts and lose_posts:
            pairs[post_text] = (win_posts, lose_posts)

    return pairs
