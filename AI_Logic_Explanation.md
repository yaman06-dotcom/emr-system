'''
# AI Health Risk Prediction: Logic and Implementation

This document explains the logic, implementation, and rationale behind the AI-powered health risk prediction feature in the EMR system.

## 1. Objective

The primary objective of the AI component is to predict a patient's risk of developing diabetes based on key health indicators. This serves as a decision support tool for doctors, helping them to identify high-risk patients who may require further screening or preventative care.

## 2. Model Selection: Logistic Regression

For this university-level project, **Logistic Regression** was chosen as the machine learning model. The reasons for this choice are:

*   **Interpretability:** Logistic Regression is a linear model, which means its results are highly interpretable. The coefficients of the model directly indicate the influence of each feature on the prediction, making it easy to explain the "why" behind a prediction. This is crucial in a medical context.
*   **Simplicity and Efficiency:** It is a computationally inexpensive and fast model to train, making it ideal for a project of this scale without requiring specialized hardware.
*   **Suitability for Binary Classification:** The problem of predicting diabetes risk (diabetic vs. non-diabetic) is a binary classification task, for which Logistic Regression is a standard and effective algorithm.
*   **Probabilistic Output:** The model outputs a probability score (from 0 to 1), which provides a more nuanced understanding of the risk rather than just a binary "yes" or "no".

## 3. Feature Selection

The model uses the following features, which are well-established risk factors for diabetes:

1.  **Age:** The risk of developing type 2 diabetes increases with age.
2.  **Body Mass Index (BMI):** Obesity is a major risk factor.
3.  **Blood Pressure (Systolic & Diastolic):** High blood pressure is often associated with insulin resistance.
4.  **Family History:** A family history of diabetes significantly increases an individual's risk.

These features are readily available in a patient's medical record.

## 4. Implementation Details

The AI logic is encapsulated within the `ai_prediction` Django app.

### `ml_model.py`

This file contains the core `HealthRiskPredictor` class, which handles model training, loading, and prediction.

*   **Training Data:** Since real patient data is not available for this project, a synthetic dataset is generated for training purposes. This data is created to reflect realistic correlations between the features and the outcome (diabetes risk).
*   **Feature Scaling:** Before training, the features are standardized using `StandardScaler` from Scikit-learn. This ensures that all features contribute equally to the model's training, preventing features with larger scales (like blood pressure) from dominating those with smaller scales (like BMI).
*   **Model Training:** A `LogisticRegression` model is trained on the scaled synthetic data. The trained model and the scaler are then saved to disk (`.pkl` files) using `joblib` for persistence.
*   **Prediction:** The `predict()` method takes a patient's data, scales it using the saved scaler, and uses the trained model to predict the probability of diabetes. This probability score is then used to classify the risk into one of three levels:
    *   **Low Risk:** Probability < 0.4
    *   **Medium Risk:** 0.4 <= Probability < 0.7
    *   **High Risk:** Probability >= 0.7

### `views.py`

The `predict_risk` view handles the web request to generate a prediction. It retrieves the patient's data, calls the `predictor.predict()` method, and saves the result (risk level, score, and recommendations) to the `HealthRiskPrediction` model in the database.

## 5. How to Use

1.  From a patient's detail page, a doctor can click the "Predict Risk" button.
2.  A form is pre-filled with the patient's latest available data (age, BMI, blood pressure).
3.  The doctor can adjust the values if needed and submit the form.
4.  The system processes the data, runs the prediction, and displays a detailed result page with the risk level and automated recommendations.

## 6. Limitations and Future Improvements

*   **Synthetic Data:** The model is trained on synthetic data, which is a significant limitation. In a real-world application, the model would need to be trained on a large, diverse, and validated dataset of actual patient records.
*   **Simple Model:** Logistic Regression is a basic model. More complex models like Gradient Boosting, Random Forests, or Neural Networks could potentially provide higher accuracy.
*   **Limited Features:** The model could be improved by including more features, such as blood glucose levels, cholesterol levels, and lifestyle factors (e.g., smoking, exercise habits).

This AI component, while simple, effectively demonstrates the integration of a machine learning model into a full-stack web application to provide valuable, data-driven insights in a clinical setting.
'''
