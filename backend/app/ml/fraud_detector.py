from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
import numpy as np
from typing import List, Dict

class FraudDetector:
    def __init__(self):
        self.isolation_forest = IsolationForest(contamination=0.1, random_state=42)
        self.lof = LocalOutlierFactor(n_neighbors=20, contamination=0.1)
        self.is_trained = False
    
    def extract_features(self, transactions: List[Dict]) -> np.ndarray:
        """Extract features from transactions"""
        features = []
        for t in transactions:
            features.append([
                t.get('amount', 0),
                t.get('hour_of_day', 0),
                t.get('days_since_last', 0),
                len(t.get('description', '')),
            ])
        return np.array(features)
    
    def train(self, transactions: List[Dict]):
        """Train fraud detector"""
        X = self.extract_features(transactions)
        
        if len(transactions) > 20:
            self.isolation_forest.fit(X)
            self.lof.fit(X)
            self.is_trained = True
    
    def detect_fraud(self, transaction: Dict) -> bool:
        """Detect if a transaction is fraudulent"""
        if not self.is_trained:
            return False
        
        feature = np.array([[
            transaction.get('amount', 0),
            transaction.get('hour_of_day', 0),
            transaction.get('days_since_last', 0),
            len(transaction.get('description', '')),
        ]])
        
        iso_pred = self.isolation_forest.predict(feature)[0]
        lof_pred = self.lof.predict(feature)[0]
        
        # Flag as fraud if both models agree
        return iso_pred == -1 and lof_pred == -1
    
    def detect_duplicate_transaction(self, transaction: Dict, recent_transactions: List[Dict]) -> bool:
        """Detect duplicate transactions"""
        for recent in recent_transactions:
            if (abs(transaction['amount'] - recent['amount']) < 0.01 and
                transaction['merchant'] == recent['merchant'] and
                transaction['category'] == recent['category']):
                return True
        return False
