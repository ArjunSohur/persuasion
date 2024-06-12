from db_creation.db_creator import main_db_creator
from db_creation.fetcher import get_op_posts

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
    
    print(len(get_op_posts("CMV.db")))

       
