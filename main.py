from db_creation.db_creator import main_db_creator
from db_creation.fetcher import get_op_posts
from hypothesis_generation.initializations import load_training_data
from hypothesis_generation.hypogeni import chai_hypogeni_alg


# ---------------------------------------------------------------------------- #
#                                                                              #
# ---------------------------------------------------------------------------- #
# Main                                                                         #
# ---------------------------------------------------------------------------- #
#                                                                              #
# ---------------------------------------------------------------------------- #

if __name__ == "__main__":
    create = 0
    main_db_creator(create)

    inital_pairs, train_pairs = load_training_data()
    
    hypothesis = chai_hypogeni_alg(inital_pairs, train_pairs, "llama3")

    print("Hypothesis bank")
    for h in hypothesis:
        print(h)
        print("\n")

    
    

       
