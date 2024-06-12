import ollama

def inference_llm(llm: str, prompt: str):
    response = ollama.chat(
    model=llm,
    messages=[{'role': 'user', 'content': prompt}])

    return response

