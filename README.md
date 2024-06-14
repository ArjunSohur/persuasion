### Read this part

The goal of this repo is to do work on persuasion and hypothesis generation - whatever that means.

I have essentially implemented Haokun's, Rosa's, and Tejes' paper (I'll refer to their work as 'HRT' from now on) on hypothesis generation (linked below), but with tailored to hypothsis generation, where the hypotheses vaguely answer "what makes a good argument".

I made a couple of changes to the way that the hypogenic algorithm works in HRT to fit it to the persuasion task.  Let's first recall the two main parts of the og HRT algorithm:

<img width="843" alt="Screenshot 2024-06-13 at 9 19 09 PM" src="https://github.com/ArjunSohur/persuasion/assets/105809809/a26ba551-3c78-46e4-bcd8-8a0c6de5243e">

<img width="352" alt="Screenshot 2024-06-13 at 9 21 13 PM" src="https://github.com/ArjunSohur/persuasion/assets/105809809/9647ad35-2758-43e7-92b3-40fad41626ed">

Now, I'll write high level pseudo-code to demonstrate how this algorithm works.

<img width="381" alt="Screenshot 2024-06-13 at 9 39 52 PM" src="https://github.com/ArjunSohur/persuasion/assets/105809809/8b7a6a09-c9de-4a7a-828a-6d11ea5176e8">

<img width="402" alt="Screenshot 2024-06-13 at 9 59 28 PM" src="https://github.com/ArjunSohur/persuasion/assets/105809809/5ee046d2-2fa9-45ef-a957-059d51f6f9ff">


### References and todo

TODO:
 - create different methods of inference
 - improve algorithm

Original corpus found at: https://convokit.cornell.edu/documentation/winning.html#

Hypothesis generation paper: https://arxiv.org/pdf/2404.04326
And their code: https://github.com/ChicagoHAI/hypothesis_generation
