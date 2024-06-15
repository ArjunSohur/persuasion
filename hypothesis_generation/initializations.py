import sys
import os
import random
import datetime

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
        ut, root = sample
        ret.append((ut, root))
    
    return ret
    

# ---------------------------------------------------------------------------- #
#                                                                              #
# ---------------------------------------------------------------------------- #
# Loading training data                                                        #
# ---------------------------------------------------------------------------- #
#                                                                              #
# ---------------------------------------------------------------------------- #

def load_training_data(num_init_pairs:int = 2, num_train_pairs:int = 3):
    loadind_dt = datetime.datetime.now()

    print("Retreiving successful (utterance, root text) tuples")
    training_pairs = get_success_posts_reply_to_text("CMV.db")

    random.shuffle(training_pairs)

    init_pairs = training_pairs[:num_init_pairs]
    train_pairs = sample_from_training_pairs(training_pairs[num_init_pairs:], num_train_pairs)

    print(f"Retreived successful (utterance, root text) tuples in {datetime.datetime.now() - loadind_dt}")

    print("Number of succesful arguments:", len(training_pairs), "\n")

    return init_pairs, train_pairs


if __name__ == "__main__":
    load_training_data()