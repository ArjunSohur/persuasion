import sqlite3
import os
from convokit import Corpus, download
import datetime

# ---------------------------------------------------------------------------- #
#                                                                              #
# ---------------------------------------------------------------------------- #
# Database functions                                                           #
# ---------------------------------------------------------------------------- #
#                                                                              #
# ---------------------------------------------------------------------------- #

def create_db():
    conn: sqlite3.Connection = sqlite3.connect("CMV.db")
    c: sqlite3.Cursor = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS CMV
                (id TEXT PRIMARY KEY, 
                root_id TEXT,
                reply_to TEXT,
                success INTEGER,
                speaker_id TEXT,
                text TEXT)''')
    conn.commit()
    conn.close()

def store_in_db(id, rootid, reply_to, success, speaker_id, text):
    conn: sqlite3.Connection = sqlite3.connect("CMV.db")
    c: sqlite3.Cursor = conn.cursor()
    c.execute("INSERT OR IGNORE INTO CMV VALUES (?, ?, ?, ?, ?, ?)", (id, rootid, reply_to, success, speaker_id, text))
    conn.commit()
    conn.close()

# ---------------------------------------------------------------------------- #
#                                                                              #
# ---------------------------------------------------------------------------- #
# Load data                                                                    #
# ---------------------------------------------------------------------------- #
#                                                                              #
# ---------------------------------------------------------------------------- #

def load_data():
    load_dt = datetime.datetime.now()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    corpus_path = os.path.join(script_dir, "winning-args-corpus")
    
    if not os.path.isdir(corpus_path):
        os.makedirs(corpus_path, exist_ok=True)
        
        print("Downloading winning-args-corpus...")
        corpus = Corpus(download("winning-args-corpus"))
        corpus.dump("winning-args-corpus", base_path=corpus_path)  # Save the corpus
    else:
        print("Loading winning-args-corpus from local storage...")
        rel_path = "winning-args-corpus/winning-args-corpus"
        corpus = Corpus(filename=rel_path)
    
    print(f"Corpus loaded: {datetime.datetime.now() - load_dt}")
    return corpus

# ---------------------------------------------------------------------------- #
#                                                                              #
# ---------------------------------------------------------------------------- #
# Process data                                                                 #
# ---------------------------------------------------------------------------- #
#                                                                              #
# ---------------------------------------------------------------------------- #
def process(corpus):
    process_dt = datetime.datetime.now()

    print("Processing data")
    utterances = list(corpus.iter_utterances())
    lengths = len(utterances)

    ids = [None]* lengths
    roots = [None]* lengths
    replies_to = [None]* lengths
    successes = [None]* lengths
    speaker_ids = [None]* lengths
    text = [None]* lengths

    for index, utterance in enumerate(utterances):
        ids[index] = utterance.id
        roots[index] = utterance.conversation_id

        replies_to[index] = utterance.reply_to

        temp_success = utterance.meta["success"]
        successes[index] = temp_success

        speaker_ids[index] = utterance.speaker.id
        text[index] = utterance.text
    
    print(f"Successfully processed data in {datetime.datetime.now() - process_dt}\n")
    
    return ids, roots, replies_to, successes, speaker_ids, text

# ---------------------------------------------------------------------------- #
#                                                                              #
# ---------------------------------------------------------------------------- #
# Store data                                                                   #
# ---------------------------------------------------------------------------- #
#                                                                              #
# ---------------------------------------------------------------------------- #
def store_data(ids, roots, replies_to, successes, speaker_ids, text):
    print("Storing data")
    for index in range(len(ids)):
        store_in_db(ids[index], roots[index], replies_to[index], \
                    successes[index], speaker_ids[index], text[index])
    print("Successfully stored data\n")


# ---------------------------------------------------------------------------- #
#                                                                              #
# ---------------------------------------------------------------------------- #
# Main Process                                                                 #
# ---------------------------------------------------------------------------- #
#                                                                              #
# ---------------------------------------------------------------------------- #
def main_db_creator(do_it: bool = True):
    main_process_dt = datetime.datetime.now()

    if not do_it:
        print("Not creating database")
        return

    create_db()
    corpus = load_data()
    ids, roots, replies_to, successes, speaker_ids, text = process(corpus)
    store_data(ids, roots, replies_to, successes, speaker_ids, text)

    print(f"Main process completed in {datetime.datetime.now() - main_process_dt}")

# Main execution
if __name__ == "__main__":
    main_db_creator()
