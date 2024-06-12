
from .prompts import get_hypothesis_generation_prompt
from .llm_ollama import inference_llm

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



def chai_hypogeni_alg(S_init, S, llm):
    H = init_H(S_init, llm)

    return H