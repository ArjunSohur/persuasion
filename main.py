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
    main_db_creator(False) 

    inital_pairs, train_pairs = load_training_data(num_init_pairs=2, num_train_pairs=6)
    
    # ollama -> llama3
    # huggingface -> meta-llama/Meta-Llama-3-8B
    H_final = hypogenic(inital_pairs, train_pairs, "meta-llama/Meta-Llama-3-8B", a=0.3, max_r=.2, topn=3)

    with open("hypothesis.txt", "w") as f:
        f.write("\n------------------------\n".join(H_final))

    null_hypothesis("hypothesis_bank.txt", "llama3", n_test=1)

    
    

       
