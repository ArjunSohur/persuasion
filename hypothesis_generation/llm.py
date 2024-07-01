from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch


class LLM:
    def __init__(self, model: str = "meta-llama/Meta-Llama-3-8B-Instruct", torch_dtype = torch.bfloat16, device_map = "cuda",
                  max_new_tokens = 256, temperature=0.6, top_p=0.9):
        self.model = model
        self.llm = pipeline("text-generation", model=model, model_kwargs={"torch_dtype": torch_dtype}, device_map=device_map)
        self.device = device_map
        self.max_new_tokens = max_new_tokens
        self.temperature = temperature
        self.top_p = top_p
    
    def inference(self, prompt, system_prompt = ""):
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ]

        # https://huggingface.co/blog/llama3
        outputs = self.llm(
            messages,
            max_new_tokens=self.max_new_tokens,
            eos_token_id= self.llm.tokenizer.eos_token_id,
            pad_token_id=self.llm.tokenizer.eos_token_id,
            do_sample=True,
            temperature=self.temperature,
            top_p=self.top_p
        )

        return outputs[0]["generated_text"][-1]["content"]