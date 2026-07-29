# ==========================================================
# HELPER FUNCTIONS
# ==========================================================

import json
import os


def load_metadata(path="model_metadata.json"):
    """Load model metadata if present, otherwise return an empty dict."""
    if not os.path.exists(path):
        return {}

    with open(path, "r") as file:
        metadata = json.load(file)

    return metadata


def risk_level(confidence):
    """Translate a confidence score into a human-friendly risk label."""
    if confidence is None:
        return "Unknown"

    if confidence >= 95:
        return "Very High"
    elif confidence >= 80:
        return "High"
    elif confidence >= 60:
        return "Medium"
    else:
        return "Low"