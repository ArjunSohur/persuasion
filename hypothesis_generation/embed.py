from sentence_transformers import SentenceTransformer
import os

def load_custom_sentence_transformer(model_name_or_path: str = "Alibaba-NLP_gte-large-en-v1.5") -> SentenceTransformer:
    """
    Loads a SentenceTransformer model (pre-trained or custom).

    Args:
        model_name_or_path: Model name (pre-trained) or path (custom) (str).

    Downloads if missing, then loads the model.

    Returns:
        Loaded SentenceTransformer model (SentenceTransformer).
    """
    # Construct the path to the torch cache directory in the user's home directory
    cache_folder = os.path.join(os.path.expanduser("~"), ".cache", "torch", "sentence_transformers")
    model_path = os.path.join(cache_folder, model_name_or_path)

    if not os.path.exists(model_path):
        print(f"Model '{model_name_or_path}' not found at '{model_path}'. Downloading...\n")
        
        os.makedirs(cache_folder, exist_ok=True)

        # I have device as cpu because I am running this on a mac - obviously, change this to gpu if you have a gpu
        model = SentenceTransformer(model_name_or_path, cache_folder=cache_folder, trust_remote_code=True, device="cuda")
        model.save(model_path)

        print("Downloading Complete, processing links ...\n")
    else:
        print(f"Model '{model_name_or_path}' found at '{model_path}'. Loading...")
        model = SentenceTransformer(model_path, cache_folder=cache_folder, trust_remote_code=True, device="cuda")
        print("Loading Complete, processing links ...\n")
    return model
