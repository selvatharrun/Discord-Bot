"""
model.py

Helper utilities to persistently store and load the YOLO model locally so it doesn't
need to be downloaded every time. Exposes:
- ensure_model(local_path): download if missing and return path
- load_model(local_path): load and return a YOLO model
- predict_face(file_path, model=None, save=True): run prediction (loads model if None)
- get_confidence(results): normalize confidences/labels into a python dict

This version avoids downloading at import time and uses a local `models/` folder.
"""
from huggingface_hub import hf_hub_download
from ultralytics import YOLO
import os
import shutil
from pathlib import Path
from typing import Optional, Dict, Any

# Configure repository and filenames
MODEL_REPO = "AdamCodd/YOLOv11n-face-detection"
MODEL_FILENAME = "model.pt"

# Default local path: <repo>/models/model.pt
BASE_DIR = Path(__file__).resolve().parent
DEFAULT_MODEL_DIR = BASE_DIR / "models"
DEFAULT_MODEL_PATH = DEFAULT_MODEL_DIR / MODEL_FILENAME


def ensure_model(local_path: Optional[os.PathLike] = None) -> str:
    """Ensure the model file exists locally. If missing, download from Hugging Face repo.

    Returns the absolute path to the model file on disk.
    """
    if local_path is None:
        local_path = DEFAULT_MODEL_PATH
    local_path = Path(local_path)
    local_path.parent.mkdir(parents=True, exist_ok=True)

    if local_path.exists():
        print(f"Model already present at {local_path}")
        return str(local_path)

    print(f"Downloading model from {MODEL_REPO}...")
    # hf_hub_download returns a path to the cached file; copy it to our models folder
    cached_file = hf_hub_download(repo_id=MODEL_REPO, filename=MODEL_FILENAME)
    shutil.copy(cached_file, local_path)
    print(f"Saved model to {local_path}")
    return str(local_path)


def load_model(local_path: Optional[os.PathLike] = None) -> YOLO:
    """Load and return a YOLO model from a persistent local path (download first if needed)."""
    model_path = ensure_model(local_path)
    print(f"Loading YOLO model from {model_path}...")
    model = YOLO(model_path)
    return model


def predict_face(file_path: str, model: Optional[YOLO] = None, save: bool = True):
    """Run model.predict on a single file. If model is None, load the persistent model.

    Returns the ultralytics Results object.
    """
    if model is None:
        model = load_model()
    results = model.predict(file_path, save=save)
    return results


def get_confidence(results) -> Dict[int, Dict[str, Any]]:
    """Extract confidences and labels from ultralytics Results into a plain dict.

    Returns a mapping: image_index -> { 'confidences': [...], 'labels': [...] }
    """
    out = {}
    for i, r in enumerate(results):
        confs = []
        labels = []
        # confidences: attempt common tensor -> numpy path, then list coercions
        try:
            confs = r.boxes.conf.cpu().numpy().tolist()
        except Exception:
            try:
                confs = [float(x) for x in r.boxes.conf]
            except Exception:
                confs = list(r.boxes.conf)

        # labels/classes if available
        if hasattr(r.boxes, "cls"):
            try:
                labels = r.boxes.cls.cpu().numpy().astype(int).tolist()
            except Exception:
                labels = list(r.boxes.cls)

        out[i] = {"confidences": confs, "labels": labels}
    return out


# Convenience export names
__all__ = [
    "ensure_model",
    "load_model",
    "predict_face",
    "get_confidence",
    "DEFAULT_MODEL_PATH",
]



