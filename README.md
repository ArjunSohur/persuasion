## Read this part

The goal of this repo is to do work on persuasion and hypothesis generation - whatever that means.

I have essentially implemented Haokun's, Rosa's, and Tejes' paper (I'll refer to their work as 'HRT' from now on) on hypothesis generation (linked below), but with tailored to hypothsis generation, where the hypotheses vaguely answer "what makes a good argument".

I made a couple of changes to the way that the hypogenic algorithm works in HRT to fit it to the persuasion task.  Let's first recall the two main parts of the og HRT algorithm:

<img width="843" alt="Screenshot 2024-06-13 at 9 19 09 PM" src="https://github.com/ArjunSohur/persuasion/assets/105809809/a26ba551-3c78-46e4-bcd8-8a0c6de5243e">

<img width="352" alt="Screenshot 2024-06-13 at 9 21 13 PM" src="https://github.com/ArjunSohur/persuasion/assets/105809809/9647ad35-2758-43e7-92b3-40fad41626ed">

Now, I'll write high level pseudo-code to demonstrate how this algorithm works.

<img width="381" alt="Screenshot 2024-06-13 at 9 39 52 PM" src="https://github.com/ArjunSohur/persuasion/assets/105809809/8b7a6a09-c9de-4a7a-828a-6d11ea5176e8">

<img width="406" alt="Screenshot 2024-06-13 at 9 59 28 PM" src="https://github.com/ArjunSohur/persuasion/assets/105809809/5ee046d2-2fa9-45ef-a957-059d51f6f9ff">

Key differences:
 - regret used as a running tally and indicator of weakness of bank
 - Keep track of worst performing samples in order to update the hypothesis bank with what it's missing
 - We actually use the hypothese to generate an argument, then compare the generated argument with the known winning argument
 - Instead of just sampling some \mathcal{S_i}, we actually iterate through all the sample pairs

Obvious shortcomings:
 - the loops are very inefficient
 - the iterating trough the training pairs is ugly
 - llm is raw, in this case (not fine tuned or pre-trained on arguments)
 - llm is slow (about 20-30 sec per inference)
 - Regret and reward grows as - I have not yet normalized them

### References and todo

TODO:
 - create different methods of inference
 - improve algorithm efficiency 

Original corpus found at: https://convokit.cornell.edu/documentation/winning.html#

Hypothesis generation paper: https://arxiv.org/pdf/2404.04326
And their code: https://github.com/ChicagoHAI/hypothesis_generation

### Note that might save some debugging
TO RUN THIS CODE, YOU MUST HAVE THE OLLAMA APP INSTALLED
https://www.ollama.com/
Ollama helps run the llm locally - alternaltively, you can edit ypothesis_generation/llm_ollama.py to use whatever method of llm inference you prefer.  I tried to make the system as llm agnostic as possible outside of the llm file.
