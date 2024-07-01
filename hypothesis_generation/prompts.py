# ---------------------------------------------------------------------------- #
#                                                                              #
# ---------------------------------------------------------------------------- #
# Hypothesis generation                                                        #
# ---------------------------------------------------------------------------- #
#                                                                              #
# ---------------------------------------------------------------------------- #
def get_hypothesis_generation_system_prompt():
    s = """You are a professional debater and philosopher.  You are currently
        studying examples of when people changed their mind and are trying to
        develop certian hypothese to see what arguments are persuasive.
        
        All of your responses should be one sentence only and should start with 
        'Arguments that...' and then continue. Mention nothing of the prompt in 
        your response.

        Here are some sample responses:
         - Arguments that are well sourced are more persuasive.
         - Arguments that use date are more persuasive.
         - Arguments that appeal to emotion are more persuasive.

        You are very determined to find the single best hypothesis.
        """
    return s

def get_hypothesis_generation_prompt(reply, op):
    s = f"""You are a professional debater and philosopher.  You are currently
        studying examples of when people changed their mind and are trying to
        develop certian hypothese to see what arguments are persuasive.  You are
        studying one particular example, at the moment:
        
        Here's the the orignal poster's arument: {op}

        Here's the reply that changed their mind: {reply}

        Your response derived from this example should be a general hypothesis 
        that could be applied to  any argument, meaning you should not discuss
        the example in your response.
        """
    
    return s

def get_new_hypothesis_generation_prompt(H_top, worst):
    hyp_list = []    
    for h in H_top:
        hyp_list.append(h[0])
    top_hypotheses = "\n".join(hyp_list) 

    V = ""

    for t in worst:
        x, y, _ = t
        v = f"Original argument: {x} \nWinning answer: {y}\n\n"
        V += v

    s = f"""You are a professinal debater and philosipher.  You are currently
        developing hypothesese for what makes a persuasive argument, however,
        you seem to have come to a dead end, as your top hypotheses don't 
        seem to be good enough.

        You do however, have a good recollection of all the arguments your 
        hypothese did particularly poorly on.

        Here they are: 
        {V}

        And here are your top hypotheses that didn't cover these arguments:
        {top_hypotheses}

        You are to now create a new hypothesis that fills in the gaps that the
        old hypothese didn't cover.

        start your response with 'Arguments that...' and then continue; if you
        don't start your response that way, you will die.

        Mention nothing of the prompt in your response - your response should 
        be one sentence only.

        Here are some sample responses:
         - Arguments that are well sourced are more persuasive.
         - Arguments that use date are more persuasive.
         - Arguments that appeal to emotion are more persuasive.

        You are very determined to find the single best hypothesis.
        """
    
    return s

# ---------------------------------------------------------------------------- #
#                                                                              #
# ---------------------------------------------------------------------------- #
# Argument production                                                          #
# ---------------------------------------------------------------------------- #
#                                                                              #
# ---------------------------------------------------------------------------- #

def get_inference_argument_prompt(op, h):
    s = f"""You are a professional debater and philosopher.  You are currently
        trying to persuade someone to change their mind, using a hypothesis
        about what makes a good argument that you developed.

        Here's the arument you're trying to rebuttle: {op}

        Here's the hypothesis you're using: {h}

        Without referencing the prompt and any way, please write your argument.
        If you reference the prompt or do say anything that doesn't
        pertain to your argument, you will die.
        """

    return s

# ---------------------------------------------------------------------------- #
#                                                                              #
# ---------------------------------------------------------------------------- #
# Null Hypothesis                                                              #
# ---------------------------------------------------------------------------- #
#                                                                              #
# ---------------------------------------------------------------------------- #
def get_null_prompt_sys():
    s = """You are a professional debater and philosopher.  You are curenntly
        trying to persuade someone to change their mind.
        
        You are very dertermined to persuade them to change their mind."""
    
    return s

def get_null_prompt(post):
    s = f"""You are a professional debater and philosopher.  You are curenntly
        trying to persuade someone to change their mind.

        Here's the argument you're trying to rebuttle: {post}"""
    
    return s

# ---------------------------------------------------------------------------- #
#                                                                              #
# ---------------------------------------------------------------------------- #
# hypothesis relevance                                                         #
# ---------------------------------------------------------------------------- #
#                                                                              #
# ---------------------------------------------------------------------------- #
def get_vector_gen_prompt(argument, hypothesis):
    s = f"""You are an advanced language model designed to evaluate the relevance of 
    hypotheses in relation to given arguments. Given an argument and a hypothesis 
    (a truism), your task is to determine if the hypothesis is germane 
    (relevant and appropriate) to the argument. If the hypothesis is germane,
    output 1. If it is not germane, output 0.

    Do not be generous with your assignment of relevance.  Only give '1' if it
    really is appropriate.

    Argument: {argument}
    Hypothesis: {hypothesis}


    YOUR OUTPUT CAN ONLY BE A 1 OR A 0.  NO OTHER WORDS OR ANYTHING IS ALLOWED.
    JUST 1 OR 0.
    """

    return s
    

