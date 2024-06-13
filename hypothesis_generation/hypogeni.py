
from .prompts import get_hypothesis_generation_prompt, get_inference_argument_prompt, get_new_hypothesis_generation_prompt
from .llm_ollama import inference_llm
from .embed import load_custom_sentence_transformer
import random
from math import sqrt, log

def init_H(S_init, llm):
    H = []

    for s in S_init:
        print("Loading initial hypothesis")
        rep, op = s
        prompt = get_hypothesis_generation_prompt(rep, op)

        response = inference_llm(llm, prompt)

        H.append(response)
        print("Loaded initial hypothesis")
    
    return H

def init_S_i(H):
    S_i = {}

    for h in H:
        S_i[h] = 1

    return S_i

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

def y_vector_gen(S, embedder):
    y_vecs = []

    for s in S:
        y, x = s
        y_vecs.append(embedder.encode(y))
    
    return y_vecs

def H_vector_gen(H, embedder, H_vecs: dict):
    for h in H:
        if h not in H_vecs:
            H_vecs[h] = embedder.encode(h)
    
    return H_vecs # in place errors?
    

def H_top(H_rewardscore, n):
    H_top_n = sorted(H_rewardscore, key=lambda x: x[1], reverse=True)
    return H_top_n[:n]

def reward(h_i, x_visited, y_visited, y_vectors, abs_S_i, t, alpha, embedder):
    numerator = 0

    worst = [(1, "", ""), (1, "", ""), (1, "", "")]

    for i, x in enumerate(x_visited):
        y_i = y_vectors[i]

        prompt = get_inference_argument_prompt(x, h_i)
        y_hat_text = inference_llm(prompt)
        y_hat = embedder.encode(y_hat_text)

        dot = y_i @ y_hat
        numerator += dot

        # see if this is among the worst examples
        for j, w in enumerate(worst):
            if dot < w[0]:
                worst[j] = (dot, x, y_visited[i])
                break

    
    if abs_S_i:
        denominator = abs_S_i
    else:
        print("Error: denominator is 0")
        return
    
    exploration = alpha * sqrt(log(t) / denominator)

    r_i = numerator / denominator + exploration

    regret = len(x_visited)/denominator - r_i

    while (1, "", "") in worst:
        worst.remove((1, "", ""))

    return r_i, regret, worst

# look at the worst performing pairs and update the worst list
def update_worst(worst, worst_i):
    temp_worst = list(set(worst.extend(worst_i)))
    for _, w in enumerate(worst_i):
        if w in worst:
            index = worst.index(w)
            worst[index][0] += 1

def get_worst(worst, n=3):
    worst = sorted(worst, key=lambda x: x[0], reverse=True)[:n]
    x = [w[1] for w in worst]
    y = [w[2] for w in worst]
    return x, y


def hypogenic(S_init, S, llm):
    n = 1
    alpha = .5
    embedder = load_custom_sentence_transformer("Alibaba-NLP_gte-large-en-v1.5")
    max_regret = 2

    H = init_H(S_init, llm)
    # H_vectors = H_vector_gen(H, embedder, {})

    y_vectors = []
    x_visited = []
    y_visited = []

    S_i = init_S_i(H)
    t = 1
    regret = 0

    H_rewardscore = None

    # the worst performing pairs with the current hypothesis
    worst = []

    for s in S:
        y_t, x_t = s
        y_vectors.append(embedder.encode(y_t))
        y_visited.append(y_t)
        x_visited.append(x_t)

        if not H_rewardscore:
            h_top = H[0]
        else:
            h_top = H_top(H_rewardscore, n)
        
        for h_i in h_top:
            S_i[h_i] += 1
            r_i, regret_i, worst_i = reward(h_i, x_visited, y_visited, y_vectors, S_i[h_i], t, alpha, embedder)

            update_worst(worst, worst_i)

            if not H_rewardscore:
                H_rewardscore = init_H_rewardscore(H, r_i, h_i)
            else:
                update_rewardscore(H_rewardscore, h_i, r_i)
            
            regret += regret_i
            
        if regret > max_regret:
            regret = 0

            worst_x, worst_y = get_worst(worst)
            
            new_h_top = H_top(H_rewardscore, n)
            prompt = get_new_hypothesis_generation_prompt(new_h_top, worst_x, worst_y)

            new_h = inference_llm(prompt)

            H.append(new_h)
            S_i[new_h] = len(worst_x)

            new_h_reward = reward(new_h, worst_x, worst_y, y_vectors, S_i[new_h], t, alpha, embedder)
            
            H_rewardscore.append((new_h, new_h_reward[0]))

        t+=1
    
    return H




