from db_creation.db_creator import main_db_creator
from hypothesis_generation.initializations import load_training_data
from hypothesis_generation.hypogeni import hypogenic
from hypothesis_generation.null_hyp import null_hypothesis


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

    main_db_creator(False) # don't want to create the database again

    inital_pairs, train_pairs = load_training_data(num_init_pairs=1, num_train_pairs=2)
    
    H_final = hypogenic(inital_pairs, train_pairs, "llama3", a=0.3, max_r=.75, topn=3)

    with open("hypothesis.txt", "w") as f:
        f.write("\n------------------------\n".join(H_final))

    null_hypothesis("hypothesis_bank.txt", "llama3", n_test=1)

    
    

       
