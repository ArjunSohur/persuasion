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

### Note that might save some debugging
TO RUN THIS CODE, YOU MUST HAVE THE OLLAMA APP INSTALLED

https://www.ollama.com/

Ollama helps run the llm locally - alternaltively, you can edit ypothesis_generation/llm_ollama.py to use whatever method of llm inference you prefer.  I tried to make the system as llm agnostic as possible outside of the llm file.

### Running the command
To run, run command at root:
```shell
python3 main.py
```

If you don't have some models downloaded, this code might do so for you.  Note that we're talking around 4 Gb of storage if you choose to use ollama's llms.

The embedder is around 2 Gb.

### Testing the null hypothesis

The way I test the null hypothesis is as follows:
1. Get hypothesis bank
2. Get data in form of "'post': ('Successful argument(s)', 'Unsuccessful argument(s)')"
3. For each line of data, do the following:\
    3a. Based on post, prompt the llm to generate a counterargument\
    3b. Find best fitting hypothesis based on cosine similarity of post and hypotheses\
    3c. Generate a counter argument uing the hypothesis\
    3d. for counter_argument in {succesful_arguments, unsuccesful_arguments}, add the cosine similarities of counter_argument and {hypothesis generated argument, raw generated argument}\
    3e. normalize the scores for each line of data
4. Done

We want to be similar to the winning argument(s) and unsimilar to losing arguemnt(s)

here are the results from running with 20 hypotheses:\
Null Hypothesis: 5.3284569120268195 for, 2.6715430879731805 against\
Hypothesis: 5.347286233735214 for, 2.6527137662647857 against

So clearly, there is no significant difference.  The problem with this method \
lies in cosine similarity itself.  From a [0, 1] scale, arguments that are somewhat \
similar but not exactly the same will score the same.  From what I noticed, it's \
all hypothesis and null generated arguments had essentially the same scores.

It's also clear that cosine similarity just doesn't capture the kind of nuance that \
defines a good argument.  In all, it's not the best metric to use here, but \
it's certainly the easiest.

As a final note on cosine similarity, I've noticed that the range of reward \
scores for hypotheses are from [50, 80], and that's being generous with the \
bounds.  If I'm going to use it extensively, which I do now, I need to find a \
way to distinguish between good and not.

### Thoughts that are worth noting (will update as I go)
As Haokun told me, the hardest part of hypothesis generation is to find wether \
a hypothesis is good or not.

I have some kind of a metric with rewrd score, but that isn't perfect, and if it \
measures anything, it's the generality of the argument.  Each hypothesis is \
applicable in a niche arguemnt which would actually lead to a better argument.

I believe that hypotheses CAN lead to llms making better arguments, the actual \
battle is finding the best hypothesis to prompt the llm.  If we think of the \
generated hypotheses as insights into debate, then the task becomes slightly \
different.

### Future directions
 - Making a way of finding best hypothesis (llm prompting ?)
 - Some kind of fine tune + pre-training of llm?
 - Research on persuasion


### References and non-urgent todo
non-urgent TODO
 - make algorithm most efficient

Original corpus found at: https://convokit.cornell.edu/documentation/winning.html#

Hypothesis generation paper: https://arxiv.org/pdf/2404.04326
And their code: https://github.com/ChicagoHAI/hypothesis_generation
