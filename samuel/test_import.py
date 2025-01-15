import pickle
import pandas as pd

person = pd.read_csv("singlerow.csv")
person = person.drop(["charges"], axis=1)

model = pickle.load(open("model.pickle", "rb"))

bins = [0, 18.5, 24.9, 29.9, 40, 100]  # Tranches de BMI
labels = ['Sous-poids', 'Poids normal', 'Surpoids', 'Obésité', 'Obésité sévère']
person['BMI_category'] = pd.cut(person['bmi'], bins=bins, labels=labels, right=False)

print(model.predict(person))

