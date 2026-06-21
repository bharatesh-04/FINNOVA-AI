from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
import numpy as np
from typing import List

class ExpenseCategorizer:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.label_encoder = LabelEncoder()
        self.is_trained = False
    
    def extract_features(self, description: str, merchant: str, amount: float) -> np.ndarray:
        """Extract features from transaction data"""
        # Simple feature extraction - can be enhanced
        features = [
            len(description),
            len(merchant),
            amount,
        ]
        return np.array(features).reshape(1, -1)
    
    def train(self, descriptions: List[str], merchants: List[str], amounts: List[float], categories: List[str]):
        """Train the classifier"""
        X = np.array([
            [len(d), len(m), a]
            for d, m, a in zip(descriptions, merchants, amounts)
        ])
        y = self.label_encoder.fit_transform(categories)
        
        self.model.fit(X, y)
        self.is_trained = True
    
    def predict(self, description: str, merchant: str, amount: float) -> str:
        """Predict category for a transaction"""
        if not self.is_trained:
            return "others"
        
        features = self.extract_features(description, merchant, amount)
        prediction = self.model.predict(features)[0]
        
        return self.label_encoder.inverse_transform([prediction])[0]
    
    def predict_with_confidence(self, description: str, merchant: str, amount: float) -> tuple:
        """Predict category with confidence score"""
        if not self.is_trained:
            return "others", 0.0
        
        features = self.extract_features(description, merchant, amount)
        probabilities = self.model.predict_proba(features)[0]
        prediction = self.model.predict(features)[0]
        confidence = max(probabilities)
        
        category = self.label_encoder.inverse_transform([prediction])[0]
        return category, confidence
