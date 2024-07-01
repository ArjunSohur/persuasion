from db_creation.db_creator import main_db_creator
from hypothesis_generation.initializations import load_training_data
from hypothesis_generation.hypogeni import hypogenic
from hypothesis_generation.null_hyp import null_hypothesis
from hypothesis_vectors.vec_gen import generate_vectos


# ---------------------------------------------------------------------------- #
#                                                                              #
# ---------------------------------------------------------------------------- #
# Main                                                                         #
# ---------------------------------------------------------------------------- #
#                                                                              #
# ---------------------------------------------------------------------------- #

create_database = False

generate_hypotheses = False
num_init_pairs = 10
num_train_pairs = 50

alpha = 0.5
max_regret = 1.0
top_n_hypotheses_in_generation = 3

generate_hypothesis_vectors = True

if __name__ == "__main__":
    if create_database:
        main_db_creator(create_database) 
    else:
        print("Not creating database from scratch")

    if generate_hypotheses:
        inital_pairs, train_pairs = load_training_data(num_init_pairs=num_init_pairs, num_train_pairs=num_train_pairs)
        
        # ollama -> llama3
        # huggingface -> meta-llama/Meta-Llama-3-8B
        H_final = hypogenic(inital_pairs, train_pairs, "meta-llama/Meta-Llama-3-8B-Instruct", a=alpha, max_r=max_regret, topn=top_n_hypotheses_in_generation)

        with open("hypothesis.txt", "w") as f:
            f.write("\n------------------------\n".join(H_final))

        null_hypothesis("hypothesis_bank.txt", "llama3", n_test=1)
    else:
        print("Not creating hypotheses from scratch")

    
    if generate_hypothesis_vectors:
        generate_vectos()

    
    

       
