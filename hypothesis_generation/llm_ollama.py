"""
Use this inferencing technique to to use a local llm.

Must have ollama installed (both the python package and the actual app)

package: https://github.com/ollama/ollama-python
app: https://www.ollama.com/

Available llms through ollama are found at https://www.ollama.com/models

I plan to include support for cloud based llms in the future, especially since
those are more robust.
"""

import ollama

def inference_llm(llm: str, prompt: str):
    response = ollama.chat(
    model=llm,
    messages=[{'role': 'user', 'content': prompt}])

    return response

