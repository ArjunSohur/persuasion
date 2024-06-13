from sentence_transformers import SentenceTransformer
import os

# ---------------------------------------------------------------------------- #
#                                                                              #
# ---------------------------------------------------------------------------- #
# Loading Embedder                                                             #
# ---------------------------------------------------------------------------- #
#                                                                              #
# ---------------------------------------------------------------------------- #

def load_custom_model(model_name_or_path: str, cache_folder: str) -> SentenceTransformer:
    """
    Loads a SentenceTransformer model (pre-trained or custom).

    Args:
        model_name_or_path: Model name (pre-trained) or path (custom) (str).
        cache_folder: Directory to cache downloaded models (str).

    Downloads if missing, then loads the model.

    Returns:
        Loaded SentenceTransformer model (SentenceTransformer).
    """
    model_path: str = os.path.join(cache_folder, model_name_or_path)

    if not os.path.exists(model_path):
        print(f"Model '{model_name_or_path}' not found at '{model_path}'. Downloading...\n")
        
        os.makedirs(model_path, exist_ok=True)

        # I have device as cpu because I am running this on a mac - obviously, change this to gpu if you have a gpu
        model: SentenceTransformer = SentenceTransformer(model_name_or_path, cache_folder=cache_folder, trust_remote_code=True, device="cpu")
        model.save(model_path)

        print("Downloading Complete, processing links ...\n")
    else:
        print(f"Model '{model_name_or_path}' found at '{model_path}'. Loading...")
        model = SentenceTransformer(model_name_or_path, cache_folder=cache_folder, trust_remote_code=True, device="cpu")
        print("Loading Complete, processing links ...\n")
    return model
