import pickle
import os
from typing import Dict
import numpy as np
import xgboost as xgb
from pathlib import Path


class LeadScoringService:
    """Service for scoring leads using XGBoost model"""
    
    def __init__(self):
        self.model_path = Path(__file__).parent.parent.parent / "ml_models" / "lead_scoring_model.pkl"
        self.model = self._load_model()
    
    def _load_model(self):
        """Load trained XGBoost model"""
        if self.model_path.exists():
            try:
                with open(self.model_path, 'rb') as f:
                    return pickle.load(f)
            except Exception:
                pass
        
        # Return a default model if none exists
        return self._create_default_model()
    
    def _create_default_model(self):
        """Create a default XGBoost model for development"""
        model = xgb.XGBClassifier(
            n_estimators=100,
            max_depth=5,
            learning_rate=0.1,
            random_state=42
        )
        
        # Train on dummy data
        X_dummy = np.random.rand(100, 10)
        y_dummy = np.random.randint(0, 2, 100)
        model.fit(X_dummy, y_dummy)
        
        return model
    
    async def score_lead(self, distress_signals: Dict) -> float:
        """Score a lead based on distress signals"""
        # Extract features from distress signals
        features = self._extract_features(distress_signals)
        
        # Predict probability
        if hasattr(self.model, 'predict_proba'):
            probability = self.model.predict_proba([features])[0][1]
        else:
            # Fallback scoring algorithm
            probability = self._calculate_score(distress_signals)
        
        return float(probability)
    
    def _extract_features(self, distress_signals: Dict) -> list:
        """Extract features from distress signals for model input"""
        return [
            float(distress_signals.get("tax_delinquent", False)),
            float(distress_signals.get("code_violations", 0)),
            1.0 if distress_signals.get("foreclosure_status") == "pre-foreclosure" else 0.0,
            1.0 if distress_signals.get("foreclosure_status") == "foreclosure" else 0.0,
            float(distress_signals.get("equity_position", 0) or 0) / 100.0,
            float(distress_signals.get("time_owned", 0) or 0) / 50.0,  # Normalize to 50 years
            float(distress_signals.get("divorce_filing", False)),
            float(distress_signals.get("bankruptcy", False)),
            float(distress_signals.get("job_loss_indicators", False)),
            1.0 if distress_signals.get("equity_position", 0) and distress_signals["equity_position"] > 20 else 0.0
        ]
    
    def _calculate_score(self, distress_signals: Dict) -> float:
        """Fallback scoring algorithm"""
        score = 0.0
        
        # Tax delinquent: +0.3
        if distress_signals.get("tax_delinquent"):
            score += 0.3
        
        # Code violations: +0.1 per violation (max 0.3)
        violations = distress_signals.get("code_violations", 0)
        score += min(0.3, violations * 0.1)
        
        # Foreclosure: +0.4
        if distress_signals.get("foreclosure_status") in ["pre-foreclosure", "foreclosure"]:
            score += 0.4
        
        # Equity position: +0.2 if >20%
        equity = distress_signals.get("equity_position", 0) or 0
        if equity > 20:
            score += 0.2
        
        # Life events: +0.1 each
        if distress_signals.get("divorce_filing"):
            score += 0.1
        if distress_signals.get("bankruptcy"):
            score += 0.1
        if distress_signals.get("job_loss_indicators"):
            score += 0.1
        
        return min(1.0, score)

