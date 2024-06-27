import os
# from .llm_ollama import inference_llm
from .llm import LLM
from .embed import load_custom_sentence_transformer
from .prompts import get_inference_argument_prompt, get_null_prompt_sys, get_null_prompt

import sys
sys.path.append("..")

from db_creation.fetcher import get_wl_pairs

sys.path.remove("..")

# ---------------------------------------------------------------------------- #
#                                                                              #
# ---------------------------------------------------------------------------- #
# Choose best hypothesis                                                       #
# ---------------------------------------------------------------------------- #
#                                                                              #
# ---------------------------------------------------------------------------- #
def choose_H(H, embedder, post):
    best_score = 0
    best_h = ""
    post_vec = embedder.encode(post)

    for h in H:
        h_vec = embedder.encode(h)
        score = post_vec @ h_vec
        if score > best_score:
            best_score = score
            best_h = h
    
    return best_h
# ---------------------------------------------------------------------------- #
#                                                                              #
# ---------------------------------------------------------------------------- #
# Get score                                                                    #
# ---------------------------------------------------------------------------- #
#                                                                              #
# ---------------------------------------------------------------------------- #
def get_score(response_vector, win, lose, embedder):
    win_score = 0
    lose_score = 0

    for item in win:
        item_vec = embedder.encode(item)
        win_score += response_vector @ item_vec
    
    for item in lose:
        item_vec = embedder.encode(item)
        lose_score += response_vector @ item_vec
    
    demoniator = win_score + lose_score

    
    return win_score/demoniator, lose_score/demoniator
    
# ---------------------------------------------------------------------------- #
#                                                                              #
# ---------------------------------------------------------------------------- #
# Test null hypothesis                                                         #
# ---------------------------------------------------------------------------- #
#                                                                              #
# ---------------------------------------------------------------------------- #
def null_hypothesis(H_Path, llm_, n_test=5):
    print(f"\nTESTING NULL HYPOTHESIS WITH {n_test} POSTS\n")

    llm = LLM(llm_)

    script_dir = os.getcwd()
    abs_file_path = os.path.join(script_dir, H_Path)

    with open(abs_file_path, 'r') as file:
        lines = file.readlines()
    
    H = []
    for line in lines:
        if not "-------------" in line:
            H.append(line.strip())
    
    print("Loading sentence transformer")
    embedder = load_custom_sentence_transformer()

    hypothesis_for = 0
    hypothesis_against = 0

    null_for = 0
    null_against = 0
    
    print("Getting win/lose pairs")
    wl_dict = get_wl_pairs("CMV.db", n=n_test)
    print("Successfully got win/lose pairs")

    for post, arguments in wl_dict.items():
        print(f"\nTesting post: {post[:100]}")
        win_posts, lose_posts = arguments

        null_prompt_sys = get_null_prompt_sys()
        null_prompt = get_null_prompt(post)
        
        print("Choosing H")
        h = choose_H(H, embedder, post)
        print("Got best H", h[:100])
        h_prompt = get_inference_argument_prompt(post, h)

        print("Awaiting LLM response")
        llm_response = llm.inference(null_prompt, system_prompt=null_prompt_sys)
        print("Got LLM response:", llm_response[:100])

        print("Awaiting Hypothesis response")
        h_response = llm.inference(h_prompt)
        print("Got Hypothesis response:", h_response[:100])

        llm_response_vector = embedder.encode(llm_response)
        h_response_vector = embedder.encode(h_response)

        print("Calculating scores")
        hyp_for, hyp_against = get_score(h_response_vector, win_posts, lose_posts, embedder)
        n_for, n_against = get_score(llm_response_vector, win_posts, lose_posts, embedder)

        hypothesis_for += hyp_for
        hypothesis_against += hyp_against

        null_for += n_for
        null_against += n_against
    
    print(f"Null Hypothesis: {null_for} for, {null_against} against")
    print(f"Hypothesis: {hypothesis_for} for, {hypothesis_against} against")

        