import random


def get_hypothesis_generation_prompt(reply, op):
    s = f"""You are a professional debater and philosopher.  You are currently
        studying examples of when people changed their mind and are trying to
        develop certian hypothese to see what arguments are persuasive.  You are
        studying one particular example, at the moment:
        
        Here's the the orignal poster's arument: {op}

        Here's the reply that changed their mind: {reply}

        Your response derived from this example should be a general hypothesis 
        that could be applied to  any argument, e.g. 'arguments that use data 
        are persuasive', 'arguments that question the premise are persuasive',
         'arguments that appeal to emotion are persuasive', etc.

        Please keep it to one sentence and do not discuss the specific example
          - in other words, keep if breif.
        
        start your response with 'Arguments that...' and then continue; if you
        don't start your response that way, you will die.

        You are very determined to find the single best hypothesis.
        """
    
    return s

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

def get_new_hypothesis_generation_prompt(H_top, x_worst, y_worst):
    top_hypotheses = "\n".join(H_top)
    V = ""

    random.sample()
    
    for i in range(len(x_worst)):
        v = f"Original argument: {x_worst[i]} \nWinning answer: {y_worst[i]}\n\n"
        V += v

    s = f"""You are a professinal debater and philosipher.  You are currently
        developing hypothesese for what makes a persuasive argument, however,
        you seem to have come to a dead end, as your top hypotheses don't 
        seem to be good enough.

        You do however, have a good recollection of all the arguments your 
        hypothese did particularly poorly on.

        Here they are: 
        {V}

        You are to now create a new hypothesis that fills in the gaps that the
        old hypothese didn't cover.

        Your new hypothesis should be in the same format as the old ones, i.e. 
        starting 'Arguments that...' and then continuing.  If you don't do this
        I will eat all your halloween candy and then you'll die.
        """
    
    return s
