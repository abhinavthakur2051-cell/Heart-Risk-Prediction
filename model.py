import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import pickle

# 1. Load data
# Make sure your heart_data.csv has these exact column names
df = pd.read_csv("heart.csv")

X = df[['age', 'gender', 'blood_pressure', 'cholesterol', 'heart_rate', 'exercise_chest_pain']]
y = df['target']

# 2. Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. Scaling (Important for accuracy)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)

# 4. Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train_scaled, y_train)

# 5. Save Model and Scaler (Dono save karne honge)
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)
with open("scaler.pkl", "wb") as f:
    pickle.dump(scaler, f)

print("✅ Model and Scaler saved successfully!")