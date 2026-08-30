import pandas as pd 
import numpy as np 
import joblib as jb 
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split 
from sklearn.metrics import confusion_matrix,ConfusionMatrixDisplay
from sklearn.metrics import classification_report
from sklearn.metrics import balanced_accuracy_score

df = pd.read_csv("C:\\Users\\Abdul Rehman\\Documents\\MLAI Related\\Python\\Python Projects\\Patient-ER-Status\\Model_Data\\er_triage_v3.csv")

df['admission_likelihood'] = df['admission_likelihood'].replace({'No': 'Low', 'Maybe': 'Moderate', 'Yes': 'High'})
df['gender'] = df['gender'].replace(['Male','Female','Other'],[0,1,2])
df['arrival_mode'] = df['arrival_mode'].replace(['Walk-in','Ambulance','Police','Transfer'],[0,1,2,3])
df['consciousness_level'] = df['consciousness_level'].replace(['Alert','Unresponsive','Pain','Voice'],[0,1,2,3])
df['chief_complaint'] = df['chief_complaint'].replace(['Chest Pain','Shortness of Breath','Laceration','Fever','Abdominal Pain','Stroke Symptoms','Prescription Refill','Severe Trauma'],[0,1,2,3,4,5,6,7])

X = df[['age','gender','arrival_mode','heart_rate','systolic_bp','diastolic_bp','respiratory_rate','spo2','temperature_c','pain_score','gcs_total','consciousness_level','chief_complaint','num_comorbidities','is_immunocompromised','num_prior_ed_visits_12m']]
Y = df['admission_likelihood']

x_train, x_test, y_train, y_test = train_test_split(X,Y, random_state = 42, test_size = 0.2,stratify=Y)

model = RandomForestClassifier(class_weight="balanced", random_state=42, n_estimators=250)

model.fit(x_train,y_train)  

model.predict(x_test)
y_pred = model.predict(x_test)

print(classification_report(y_test,y_pred))

bas = balanced_accuracy_score(y_test,y_pred)
print(bas)


cm = confusion_matrix(y_test, y_pred, labels=['Low', 'Moderate', 'High'])
cd = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['Low', 'Moderate', 'High'])
cd.plot(cmap='Reds')
plt.title('admission_likelihood Confusion Matrix')
plt.show()

jb.dump(model, 'admission_likelihood.pkl')
print('Success!')