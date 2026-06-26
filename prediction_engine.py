import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor

class StartupPredictor:
    def __init__(self, df):
        self.df = df.copy()
        self.label_encoders = {}
        self.models = {}

    def preprocess(self):
        # Encode categorical columns
        for col in ['Country', 'Industry']:
            le = LabelEncoder()
            self.df[col + '_enc'] = le.fit_transform(self.df[col])
            self.label_encoders[col] = le

        # Final features (ONLY 4 features)
        self.features = ['Country_enc', 'Industry_enc', 'Number of Employees', 'Year']
        self.target = 'Amount Raised (USD)'

        self.X = self.df[self.features]
        self.y = self.df[self.target]

    def train_models(self):
        model = RandomForestRegressor(n_estimators=100)
        model.fit(self.X, self.y)
        self.models['rf'] = model

    def predict_next(self, startup_info):
        # Convert input to model format (EXACT SAME 4 FEATURES)
        X = []

        X.append(self.label_encoders['Country'].transform([startup_info['Country']])[0])
        X.append(self.label_encoders['Industry'].transform([startup_info['Industry']])[0])
        X.append(float(startup_info['Number of Employees']))
        X.append(float(startup_info['Funding Year']))

        X = np.array(X).reshape(1, -1)

        prediction = self.models['rf'].predict(X)[0]
        return prediction