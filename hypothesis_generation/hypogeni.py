
from .prompts import get_hypothesis_generation_prompt, get_inference_argument_prompt, get_new_hypothesis_generation_prompt
from .llm_ollama import inference_llm
from .embed import load_custom_sentence_transformer
import random
from math import sqrt, log

# ---------------------------------------------------------------------------- #
#                                                                              #
# ---------------------------------------------------------------------------- #
# Initialization functions - H and S_i                                         #
# ---------------------------------------------------------------------------- #
#                                                                              #
# ---------------------------------------------------------------------------- #
def init_H(S_init, llm):
    H = []

    for s in S_init:
        rep, op = s
        prompt = get_hypothesis_generation_prompt(rep, op)

        response = inference_llm(llm, prompt)

        H.append(response)
    
    return H

def init_S_i(H):
    S_i = {}

    for h in H:
        S_i[h] = 1

    return S_i

# ---------------------------------------------------------------------------- #
#                                                                              #
# ---------------------------------------------------------------------------- #
# Reward scores                                                                #
# ---------------------------------------------------------------------------- #
#                                                                              #
# ---------------------------------------------------------------------------- #
def init_H_rewardscore(H, r, h_i):
    H_rewardscore = []
    for h in H:
        if h != h_i:
            H_rewardscore.append((h, r + random.random()/100))
        else: 
            H_rewardscore.append((h, r))
    
    return H_rewardscore

def update_rewardscore(H_rewardscore, h_i, r):
    for i, h in enumerate(H_rewardscore):
        if h[0] == h_i:
            H_rewardscore[i] = (h_i, r)
            break

    return H_rewardscore

# ---------------------------------------------------------------------------- #
#                                                                              #
# ---------------------------------------------------------------------------- #
# Hypothesis cleansing                                                         #
# ---------------------------------------------------------------------------- #
#                                                                              #
# ---------------------------------------------------------------------------- #
def H_vector_gen(H, embedder, H_vecs = {}):
    for h in H:
        H_vecs[h] = embedder.encode(h)
    
    return H_vecs

def remove_duplicates(H: list, H_vecs: dict):
    # if vectors are too, similar, remove one of the hypotheses
    # also, I was silly to make H_vecs a dict - I thought I would need to, but I guess not
    to_delete = []

    for hypothesis, vector in H_vecs.items():

        for h_i in H:
            if not hypothesis == h_i and not (hypothesis in to_delete):

                vector_2 = H_vecs[h_i]
                norms = sqrt(vector @ vector) * sqrt(vector_2 @ vector_2)
                css = (vector @ vector_2) / norms

                if css > .90: # hyperparam
                    # remove h_i from H and H_vecs

                    print(f"\nRemoving '{h_i}' from hypotheses - too similar to '{hypothesis}'")

                    H.remove(h_i)
                    
                    to_delete.append(h_i)
    
    for delete in to_delete:
        H_vecs.pop(delete)

    return H, H_vecs

# ---------------------------------------------------------------------------- #
#                                                                              #
# ---------------------------------------------------------------------------- #
# Top H                                                                        #
# ---------------------------------------------------------------------------- #
#                                                                              #
# ---------------------------------------------------------------------------- #
def H_top(H_rewardscore, n, H):
    if not H_rewardscore:
        return [(H[0], .00001)]

    H_top_n = sorted(H_rewardscore, key=lambda x: x[1], reverse=True)
    return H_top_n[:n]

# ---------------------------------------------------------------------------- #
#                                                                              #
# ---------------------------------------------------------------------------- #
# Worst examples                                                               #
# ---------------------------------------------------------------------------- #
#                                                                              #
# ---------------------------------------------------------------------------- #
"""
In order to address the weaknesses of our current hypothesis banks, we need to
see what the worst performing examples are to update the hypothesis bank.
"""
def update_worst(worst: dict, worst_i: list):
    if not worst:
        worst = {} # just to be explicit
        for w in worst_i:
            x, y, score = w
            worst[x] = (x, y, score)
        return worst

    # I don't like that this is n^2, but I'm too lazy to fix it right now
    for _, w in enumerate(worst_i):
        x, y, score = w

        if x in worst:
            X, Y, S = worst[x]
            worst[x] = (X, Y, S + score)
        else:
            worst[x] = (x, y, score)
    
    return worst

def get_worst(worst: dict, n=3):
    worst_n = []
    for _, value in worst.items():
        x, y, score = value
        worst_n.append((x, y, score))
    
    return sorted(worst_n, key=lambda x: x[2], reverse=True)[:n]



# ---------------------------------------------------------------------------- #
#                                                                              #
# ---------------------------------------------------------------------------- #
# Reward                                                                       #
# ---------------------------------------------------------------------------- #
#                                                                              #
# ---------------------------------------------------------------------------- #
"""
The reward function is used to determine how well a hypothesis is performing.
"""
def reward(h_i, x_visited, y_visited, y_vectors, abs_S_i, t, alpha, embedder, llm):
    numerator = 0

    # initalizing the worst examples
    worst = [("", "", 10000000), ("", "", 10000000), ("", "", 10000000)]

    for i, x in enumerate(x_visited):
        y_i = y_vectors[i]

        prompt = get_inference_argument_prompt(x, h_i)
        y_hat_text = inference_llm(llm, prompt)
        y_hat = embedder.encode(y_hat_text)

        dot = y_i @ y_hat
        norm = sqrt(y_i @ y_i) * sqrt(y_hat @ y_hat)

        css = dot/norm

        numerator += css

        # see if this is among the worst examples
        for j, w in enumerate(worst):
            if css < w[2]:
                worst[j] = (x, y_visited[i], 1-css)
                break

    if abs_S_i:
        denominator = abs_S_i
    else:
        print("Error: denominator is 0")
        return
    
    exploration = alpha * sqrt(log(t) / denominator)

    r_i = numerator / denominator + exploration

    regret_mag = len(x_visited)/denominator - r_i + exploration

    while ("", "", 10000000)in worst:
        worst.remove(("", "", 10000000))

    normalizer = r_i + regret_mag

    reward = r_i / normalizer
    regret = regret_mag / normalizer

    return reward, regret, list(set(worst))

# ---------------------------------------------------------------------------- #
#                                                                              #
# ---------------------------------------------------------------------------- #
# MAIN ALGORITHM                                                               #
# ---------------------------------------------------------------------------- #
#                                                                              #
# ---------------------------------------------------------------------------- #
"""
Hypothesis generation surrounding persuasion

Variables:
    n: number of top hypotheses to consider
    alpha: exploration constant
    embedder: sentence transformer model.  I use Alibaba-NLP_gte-large-en-v1.5
    max_regret: maximum regret allowed before generating a new hypothesis

    H: list of hypotheses
    S_i: dictionary of hypothesis and the number of times they have been visited
        used to calculate the reward

    y_vectors: list of vectors for y - used to measure hypothesis performance
    x_visited: list of posts visited
    y_visited: list of succesful responses visited
    
    t: time step
    regret: how poorly top hypotheses are performing

    H_rewardscore: list of tuples of hypothesis and their reward scores

    worst: list of the worst performing pairs with the current hypothesis
"""
def hypogenic(S_init, S, llm):
    """
    Hypothesis generation for persuasion

    Args:
        S_init: list of tuples of prompt and response for initial hypotheses
        S: list of tuples of prompt and successful response
        llm: language model
    
    Returns:
        H: list of hypotheses
    """
    n = 1
    alpha = 0.2
    embedder = load_custom_sentence_transformer("Alibaba-NLP_gte-large-en-v1.5")
    max_regret = .4

    print("Initializing hypotheses...")
    H = init_H(S_init, llm)
    S_i = init_S_i(H)

    y_vectors = []
    x_visited = []
    y_visited = []

    t = 1
    regret = 0

    H_rewardscore = None

    worst = {}

    print("Generating initial hypothesis vectors...")
    H_vecs: dict = H_vector_gen(H, embedder)

    for s in S:
        y_t, x_t = s
        y_vectors.append(embedder.encode(y_t))
        y_visited.append(y_t)
        x_visited.append(x_t)

        print(f"\nTime step {t}")
        print(f"{t}: Top hypotheses: {H_top(H_rewardscore, n, H)}")
        toph = H_top(H_rewardscore, n, H)

        for hypothesis in toph:
            h_i = hypothesis[0]
            print(f"{t}: Calculating reward for hypothesis '{h_i[:100]}'")

            S_i[h_i] += 1
            r_i, regret_i, worst_i = reward(h_i, x_visited, y_visited, y_vectors, S_i[h_i], t, alpha, embedder, llm)
            print(f"\t{t}: Reward: {r_i}, Regret: {regret_i}")
            
            worst = update_worst(worst, worst_i)

            if not H_rewardscore:
                H_rewardscore = init_H_rewardscore(H, r_i, h_i)
                print(f"{t}: Initialized reward scores. First element: {H_rewardscore[0][1]}: {H_rewardscore[0][0][:100]}")
            else:
                update_rewardscore(H_rewardscore, h_i, r_i)
                print(f"{t}: Updated reward scores. First element: {H_rewardscore[0][1]}: {H_rewardscore[0][0][:100]}")
            
            regret += regret_i
            print(f"{t}: Current total regret: {regret}")
            
        if regret > max_regret:
            print(f"{t}: Regret exceeded max threshold, generating new hypothesis...")
            regret = 0

            worst_3 = get_worst(worst, n=3)

            worst_x = [w[0] for w in worst_3]
            worst_y = [w[1] for w in worst_3]
            
            new_h_top = H_top(H_rewardscore, n, H)
            prompt = get_new_hypothesis_generation_prompt(new_h_top, worst_3)

            new_h = inference_llm(llm, prompt)
            print(f"{t}: Generated new hypothesis: '{new_h[:100]}'")

            H.append(new_h)
            S_i[new_h] = len(worst_3)

            print("calculating reward for new hypothesis...")
            new_h_reward, new_h_regret, new_h_worst = reward(new_h, worst_x, worst_y, y_vectors, S_i[new_h], t, alpha, embedder, llm)
            print(f"{t}: New hypothesis reward: {new_h_reward}")

            worst = update_worst(worst, new_h_worst)

            H_rewardscore.append((new_h, new_h_reward))
            print(f"{t}: Updated hypothesis reward scores afer adding new hypothesis. First element: {H_rewardscore[0][1]}: {H_rewardscore[0][0][:100]}")

            H_vecs[new_h] = embedder.encode(new_h)

            H, H_vecs = remove_duplicates(H, H_vecs)

        t += 1
    
    print("Hypothesis reward scores:")
    for h in H_rewardscore:
        print(f"  - {h[0]}: {h[1]}")
    
    return H





