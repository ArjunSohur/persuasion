import sys
import os
import random

# Add the project root to sys.path to handle the relative imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db_creation.fetcher import get_success_posts_reply_to_text

# ---------------------------------------------------------------------------- #
#                                                                              #
# ---------------------------------------------------------------------------- #
# Convenient Functions                                                         #
# ---------------------------------------------------------------------------- #
#                                                                              #
# ---------------------------------------------------------------------------- #
def sample_from_training_pairs(pairs, n):
    sampled = random.sample(pairs, n)
    ret = []

    for sample in sampled:
        ut, reply, root = sample
        ret.append((ut[:100], reply[:100], root[:100]))
    
    return ret
    

# ---------------------------------------------------------------------------- #
#                                                                              #
# ---------------------------------------------------------------------------- #
# Loading training data                                                        #
# ---------------------------------------------------------------------------- #
#                                                                              #
# ---------------------------------------------------------------------------- #

def load_training_data():
    print("Retreiving successful (utterance, reply to, root text) tuples")
    training_pairs = get_success_posts_reply_to_text("CMV.db")
    print("Retreived successful (utterance, reply to, root text) tuples\n")

    print("Number of succesful arguments:", len(training_pairs))



if __name__ == "__main__":
    load_training_data()