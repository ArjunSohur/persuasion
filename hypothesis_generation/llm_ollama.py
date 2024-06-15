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
from ollama import _client, _types
import datetime

def handle_expection(e, llm) -> bool:
    print(f"Error: {e}")
    if 'not found' in str(e):
        try:
            download_dt = datetime.datetime.now()
            print(f"\t{llm} not found - Attempting to pull {llm}")
            s = ollama.pull(llm)
            print(f"\tDownload status: {s} in {datetime.datetime.now() - download_dt}")
            return True
        except e:
            print(f"Failed to pull {llm}")
            return False
        
    print("inferece failed")
    return False

def inference_llm(llm: str, prompt: str, sys_prompt: str = None):
    try_inference = True

    while try_inference:
        inderence_dt = datetime.datetime.now()
        print("\t\tAttempting inference")
        if  not sys_prompt:
            try:
                response = ollama.chat(
                model=llm,
                messages=[{'role': 'user', 'content': prompt}])
                try_inference = False
            except _types.ResponseError as e:
                try_inference = handle_expection(e, llm)
        else:
            try:
                response = ollama.chat(
                model=llm,
                messages=[{'role': 'system', 'content': sys_prompt}, {'role': 'user', 'content': prompt}])
                try_inference = False
            except _types.ResponseError as e:
                try_inference = handle_expection(e, llm)
        print(f"\t\t\tInference complete in {datetime.datetime.now() - inderence_dt}")
            
    return response['message']['content']

