from db_creation.fetcher import get_simple_data
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from hypothesis_generation.prompts import get_vector_gen_prompt
import datetime
from hypothesis_generation.llm import LLM

import random
import pickle

def get_hypotheses():
    s = ""
    with open("hypothesis.txt", "r") as f:
        s = f.read()
    
    hypotheses = s.split("\n------------------------\n")

    return hypotheses

def pickings(hypotheses, data, dictionary):
    llm = LLM(temperature=0.3)

    length = len(data)

    start_t = datetime.datetime.now()

    counter = 0
    
    cycle_t = datetime.datetime.now()

    for datum in data:
        og, _, success = datum
        good = True
        answers = []

        for h in hypotheses:
            out = 0
            p = get_vector_gen_prompt(og, h)
            try:
                s = llm.inference(p)
                out = int(s)
                answers += [(h, out)]
            except:
                print(f"Ungood llm generation", out)
                good = False
        
        if counter % 10 == 0:
            end_t = datetime.datetime.now()
            print(f"{counter}/{length} in {end_t - cycle_t}")
            cycle_t = end_t

        if good:
            for hypothesis, score in answers:
                if hypothesis != "success":
                    dictionary[hypothesis] = dictionary[hypothesis] + [score]

            dictionary["success"] += [success]

        counter += 1
    
    print(f"Finished vectorization process in {datetime.datetime.now() - start_t}")

    


def generate_vectos():
    H = get_hypotheses()

    H.append("success")

    d = {key: [] for key in H}

    data = get_simple_data("CMV.db")

    random.shuffle(data)

    pickings(H, data, d)

    print(d["success"])

    with open('saved_dictionary.pkl', 'wb') as f:
        pickle.dump(d, f)





