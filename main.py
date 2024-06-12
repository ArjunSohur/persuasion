from db_creation.db_creator import main_db_creator
from db_creation.fetcher import get_op_posts
from hypothesis_generation.initializations import load_training_data


# ---------------------------------------------------------------------------- #
#                                                                              #
# ---------------------------------------------------------------------------- #
# Main                                                                         #
# ---------------------------------------------------------------------------- #
#                                                                              #
# ---------------------------------------------------------------------------- #

if __name__ == "__main__":
    create = 0

    if create:
        main_db_creator()
    else:
        print("Not creating database")
    
    inital_pairs, train_pairs = load_training_data()

    
    

       
