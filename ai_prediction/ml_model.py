"""
AI Health Risk Prediction Module
Uses Logistic Regression to predict diabetes risk based on patient health metrics
"""

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import joblib
import os
from django.conf import settings


class HealthRiskPredictor:
    """
    Health Risk Prediction using Logistic Regression
    
    Features:
    - Age (years)
    - BMI (Body Mass Index)
    - Blood Pressure Systolic (mmHg)
    - Blood Pressure Diastolic (mmHg)
    - Family History (binary: 0 or 1)
    
    Risk Levels:
    - Low Risk: probability < 0.4
    - Medium Risk: 0.4 <= probability < 0.7
    - High Risk: probability >= 0.7
    """
    
    def __init__(self):
        self.model = None
        self.scaler = None
        self.model_version = "1.0"
        self.model_path = os.path.join(settings.BASE_DIR, 'ai_prediction', 'trained_model.pkl')
        self.scaler_path = os.path.join(settings.BASE_DIR, 'ai_prediction', 'scaler.pkl')
    
    def train_model(self):
        """
        Train the model with synthetic training data
        In a real-world scenario, this would use actual patient data
        """
        # Synthetic training data (features: age, bmi, bp_systolic, bp_diastolic, family_history)
        # Labels: 0 = no diabetes, 1 = diabetes
        
        # Generate synthetic training data
        np.random.seed(42)
        
        # Low risk patients
        low_risk = np.column_stack([
            np.random.normal(35, 10, 100),  # age
            np.random.normal(22, 2, 100),   # bmi
            np.random.normal(115, 10, 100), # systolic
            np.random.normal(75, 8, 100),   # diastolic
            np.random.binomial(1, 0.1, 100) # family history
        ])
        low_risk_labels = np.zeros(100)
        
        # Medium risk patients
        medium_risk = np.column_stack([
            np.random.normal(50, 10, 100),  # age
            np.random.normal(27, 2, 100),   # bmi
            np.random.normal(130, 10, 100), # systolic
            np.random.normal(85, 8, 100),   # diastolic
            np.random.binomial(1, 0.4, 100) # family history
        ])
        medium_risk_labels = np.random.binomial(1, 0.5, 100)
        
        # High risk patients
        high_risk = np.column_stack([
            np.random.normal(60, 8, 100),   # age
            np.random.normal(32, 3, 100),   # bmi
            np.random.normal(145, 10, 100), # systolic
            np.random.normal(95, 8, 100),   # diastolic
            np.random.binomial(1, 0.7, 100) # family history
        ])
        high_risk_labels = np.ones(100)
        
        # Combine all data
        X_train = np.vstack([low_risk, medium_risk, high_risk])
        y_train = np.hstack([low_risk_labels, medium_risk_labels, high_risk_labels])
        
        # Standardize features
        self.scaler = StandardScaler()
        X_train_scaled = self.scaler.fit_transform(X_train)
        
        # Train Logistic Regression model
        self.model = LogisticRegression(random_state=42, max_iter=1000)
        self.model.fit(X_train_scaled, y_train)
        
        # Save model and scaler
        joblib.dump(self.model, self.model_path)
        joblib.dump(self.scaler, self.scaler_path)
        
        print(f"Model trained successfully!")
        print(f"Training accuracy: {self.model.score(X_train_scaled, y_train):.2f}")
    
    def load_model(self):
        """
        Load the trained model and scaler
        """
        if os.path.exists(self.model_path) and os.path.exists(self.scaler_path):
            self.model = joblib.load(self.model_path)
            self.scaler = joblib.load(self.scaler_path)
            return True
        return False
    
    def predict(self, age, bmi, bp_systolic, bp_diastolic, has_family_history):
        """
        Predict diabetes risk for a patient
        
        Args:
            age: Patient age in years
            bmi: Body Mass Index
            bp_systolic: Systolic blood pressure (mmHg)
            bp_diastolic: Diastolic blood pressure (mmHg)
            has_family_history: Boolean indicating family history of diabetes
        
        Returns:
            tuple: (risk_level, risk_score)
                risk_level: 'LOW', 'MEDIUM', or 'HIGH'
                risk_score: probability score (0-1)
        """
        # Load model if not already loaded
        if self.model is None:
            if not self.load_model():
                self.train_model()
        
        # Prepare input features
        family_history_binary = 1 if has_family_history else 0
        features = np.array([[age, bmi, bp_systolic, bp_diastolic, family_history_binary]])
        
        # Standardize features
        features_scaled = self.scaler.transform(features)
        
        # Predict probability
        risk_score = self.model.predict_proba(features_scaled)[0][1]
        
        # Determine risk level
        if risk_score < 0.4:
            risk_level = 'LOW'
        elif risk_score < 0.7:
            risk_level = 'MEDIUM'
        else:
            risk_level = 'HIGH'
        
        return risk_level, round(risk_score, 4)
    
    def get_feature_importance(self):
        """
        Get feature importance (coefficients) from the model
        """
        if self.model is None:
            if not self.load_model():
                return None
        
        feature_names = ['Age', 'BMI', 'BP Systolic', 'BP Diastolic', 'Family History']
        coefficients = self.model.coef_[0]
        
        importance = dict(zip(feature_names, coefficients))
        return importance


# Initialize global predictor instance
predictor = HealthRiskPredictor()
