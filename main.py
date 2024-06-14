from db_creation.db_creator import main_db_creator
from db_creation.fetcher import get_op_posts
from hypothesis_generation.initializations import load_training_data
from hypothesis_generation.hypogeni import hypogenic


# ---------------------------------------------------------------------------- #
#                                                                              #
# ---------------------------------------------------------------------------- #
# Main                                                                         #
# ---------------------------------------------------------------------------- #
#                                                                              #
# ---------------------------------------------------------------------------- #

if __name__ == "__main__":
    print("NOTE: TO RUN THIS CODE, YOU MUST HAVE THE OLLAMA APP INSTALLED")
    print("https://www.ollama.com/")
    print("Ollama helps run the llm locally - alternaltively, you can edit hypothesis_generation/llm_ollama.py to use whatever method of llm inference you prefer.\n\n")

    create = 0
    main_db_creator(create)

    inital_pairs, train_pairs = load_training_data()
    
    hypothesis = hypogenic(inital_pairs, train_pairs, "llama3")

    
    

       
