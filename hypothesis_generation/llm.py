from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch


class LLM:
    def __init__(self, model: str, torch_dtype = torch.bfloat16, device_map = "cuda"):
        self.model = model
        self.llm = pipeline("text-generation", model=model, model_kwargs={"torch_dtype": torch_dtype}, device_map=device_map)
        self.device = device_map
    
    def inference(self, prompt, system_prompt = ""):
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ]

        # https://huggingface.co/blog/llama3
        outputs = self.llm(
            messages,
            max_new_tokens=256,
            eos_token_id= self.llm.tokenizer.eos_token_id,
            pad_token_id=self.llm.tokenizer.eos_token_id,
            do_sample=True,
            temperature=0.6,
            top_p=0.9,
        )

        return outputs[0]["asistant"]["context"]