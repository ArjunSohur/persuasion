from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch


class LLM:
    def __init__(self, model: str, torch_dtype = torch.bfloat16, device_map = "cuda"):
        self.model = model
        self.llm = pipeline("text-generation", model=model, model_kwargs={"torch_dtype": torch_dtype}, device_map=device_map)
        self.device = device_map
    
    def inference(self, prompt, system_prompt = ""):
        combined_prompt = system_prompt + "\n" + prompt
        return self.llm(combined_prompt)