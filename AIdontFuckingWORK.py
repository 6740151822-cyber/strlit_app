import json
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import numpy as np

data = {
    "translation": "Der Lehrer gibt dem Schüler ein Buch und eine Blume.",
    "Nominativ": ["der Lehrer"],
    "Akkusativ": ["ein Buch", "eine Blume"],
    "Dativ": ["dem Schüler"],
    "Genitiv": [],
    "maskulin": 2,
    "neutral": 1,
    "feminin": 1
}




#turn into list again cuz using raw file will crash if its wrong and cuz ai is stupid
nominativList = data.get("Nominativ") or []
akkusativList = data.get("Akkusativ") or []
dativList = data.get("Dativ") or []
genetivList = data.get("Genitiv") or []
translation = data.get("translation", "Translation not available.")
maskulin = data.get("maskulin")
neutral = data.get("neutral")
feminin = data.get("feminin")

#padding the list with None cuz dataframe have to be the same length
maxLength = max(len(nominativList), len(akkusativList), len(dativList), len(genetivList))

nominativList += [None] * (maxLength - len(nominativList))
akkusativList += [None] * (maxLength - len(akkusativList))
dativList += [None] * (maxLength - len(dativList))
genetivList += [None] * (maxLength - len(genetivList))

dictData = {
    "Nominativ" : nominativList,
    "Akkusativ" : akkusativList,
    "Dativ" : dativList,
    "Genetiv" : genetivList}
df = pd.DataFrame(dictData)
df.index = range(1, len(df) + 1)
df = df.fillna("----")

genderData = {
    "Maskulin" : maskulin,
    "Neutral" : neutral,
    "Feminin" : feminin
}

labels = genderData.keys()
sizes = genderData.values()
colors = ["blue", "green", "pink"]
def OuterPercentCount(values):
    def InnerPercentCount(pct):
        total = sum(values)
        count = int(round(pct*total/100.0))
        return f"{count} ({pct:.1f}%)"
    return InnerPercentCount

plt.figure(figsize=(6,6))
plt.pie(sizes, labels=labels, autopct=OuterPercentCount(sizes), colors=colors,)
plt.title("German Gender Pie Chart")
plt.show()

print("\nGerman translation:")
print(translation)

print("\nNoun Case DataFrame (with articles):")
print(df)

