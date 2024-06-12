


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

        You are very determined to find the single best hypothesis.
        """