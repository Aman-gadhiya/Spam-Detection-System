# ==========================================================
# AI SPAM DETECTOR
# PREDICTION ENGINE
# ==========================================================

import os
import pickle


class SpamPredictor:

    def __init__(self, pipeline_path):
        base_dir = Path(__file__).resolve().parent
        self.pipeline_path = base_dir / pipeline_path
        self.pipeline = None
        self.load_pipeline()

    # ------------------------------------------------------
    # LOAD MODEL
    # ------------------------------------------------------
    def load_pipeline(self):
        if not self.pipeline_path.exists():
            raise FileNotFoundError(f"Model not found: {self.pipeline_path}")

        with open(self.pipeline_path, "rb") as file:
            self.pipeline = pickle.load(file)

    # ------------------------------------------------------
    # PREDICT
    # ------------------------------------------------------
    def predict(self, message):
        return self.pipeline.predict([message])[0]

    # ------------------------------------------------------
    # PREDICT PROBABILITY
    # ------------------------------------------------------
    def predict_probability(self, message):
        classifier = self.pipeline.named_steps.get("classifier")

        if classifier is not None and hasattr(classifier, "predict_proba"):
            return self.pipeline.predict_proba([message])[0]

        return None

    # ------------------------------------------------------
    # COMPLETE ANALYSIS
    # ------------------------------------------------------
    def analyze(self, message):
        prediction = self.predict(message)
        probabilities = self.predict_probability(message)

        confidence = float(max(probabilities) * 100) if probabilities is not None else None

        return {
            "prediction": prediction,
            "label": "Safe" if prediction == 0 else "Spam",
            "confidence": confidence,
            "probabilities": probabilities,
        }
