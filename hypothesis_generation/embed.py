from sentence_transformers import SentenceTransformer
import os

def load_custom_sentence_transformer(model_name_or_path: str = "Alibaba-NLP-gte-large-en-v1.5") -> SentenceTransformer:
    """
    Loads a SentenceTransformer model (pre-trained or custom).

    Args:
        model_name_or_path: Model name (pre-trained) or path (custom) (str).

    Downloads if missing, then loads the model.

    Returns:
        Loaded SentenceTransformer model (SentenceTransformer).
    """
    # I have device as cuda because I am running this on a gou - obviously, change this to cpu if you have a cpu
    model = SentenceTransformer("Alibaba-NLP/gte-large-en-v1.5", cache_folder=cache_folder, trust_remote_code=True, device="cuda")
    model.save(model_path)

    print("Downloading Complete, processing links ...\n")

    return model
