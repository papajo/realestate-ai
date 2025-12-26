"""
Train XGBoost model for lead scoring
"""
import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score
import pickle
import os
from pathlib import Path


def generate_sample_data(n_samples=1000):
    """Generate sample training data"""
    np.random.seed(42)
    
    data = {
        'tax_delinquent': np.random.choice([0, 1], n_samples, p=[0.7, 0.3]),
        'code_violations': np.random.poisson(1, n_samples),
        'foreclosure_pre': np.random.choice([0, 1], n_samples, p=[0.9, 0.1]),
        'foreclosure_active': np.random.choice([0, 1], n_samples, p=[0.95, 0.05]),
        'equity_position': np.random.uniform(0, 100, n_samples),
        'time_owned': np.random.uniform(0, 50, n_samples),
        'divorce_filing': np.random.choice([0, 1], n_samples, p=[0.95, 0.05]),
        'bankruptcy': np.random.choice([0, 1], n_samples, p=[0.97, 0.03]),
        'job_loss': np.random.choice([0, 1], n_samples, p=[0.9, 0.1]),
        'high_equity': np.random.choice([0, 1], n_samples, p=[0.6, 0.4]),
    }
    
    df = pd.DataFrame(data)
    
    # Generate target (high-value lead) based on features
    df['target'] = (
        (df['tax_delinquent'] * 0.3) +
        (df['code_violations'] * 0.1) +
        (df['foreclosure_pre'] * 0.4) +
        (df['foreclosure_active'] * 0.5) +
        (df['divorce_filing'] * 0.1) +
        (df['bankruptcy'] * 0.1) +
        (df['job_loss'] * 0.1) +
        (df['high_equity'] * 0.2) +
        np.random.normal(0, 0.1, n_samples)
    )
    
    df['target'] = (df['target'] > 0.5).astype(int)
    
    return df


def train_model():
    """Train XGBoost model"""
    print("Generating sample data...")
    df = generate_sample_data(n_samples=5000)
    
    # Prepare features and target
    feature_cols = [
        'tax_delinquent', 'code_violations', 'foreclosure_pre', 'foreclosure_active',
        'equity_position', 'time_owned', 'divorce_filing', 'bankruptcy', 'job_loss', 'high_equity'
    ]
    
    X = df[feature_cols]
    y = df['target']
    
    # Normalize equity_position and time_owned
    X['equity_position'] = X['equity_position'] / 100.0
    X['time_owned'] = X['time_owned'] / 50.0
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Train model
    print("Training XGBoost model...")
    model = xgb.XGBClassifier(
        n_estimators=100,
        max_depth=5,
        learning_rate=0.1,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        eval_metric='logloss'
    )
    
    model.fit(
        X_train, y_train,
        eval_set=[(X_test, y_test)],
        verbose=False
    )
    
    # Evaluate
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    
    accuracy = accuracy_score(y_test, y_pred)
    auc = roc_auc_score(y_test, y_pred_proba)
    
    print(f"\nModel Performance:")
    print(f"Accuracy: {accuracy:.4f}")
    print(f"AUC-ROC: {auc:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    # Save model
    model_dir = Path(__file__).parent
    model_path = model_dir / "lead_scoring_model.pkl"
    
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    
    print(f"\nModel saved to {model_path}")
    
    return model


if __name__ == "__main__":
    train_model()

