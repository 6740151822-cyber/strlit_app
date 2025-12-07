import streamlit as st
import pandas as pd
import numpy as np
import google.generativeai as genai
import os
import json
import matplotlib.pyplot as plt 
import plotly.express as px

api_key = st.sidebar.text_input("Enter your Google Generative AI API Key:", type="password")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.5-flash-lite")
generation_config = {"temperature": 0.2}


st.title("ENG to GER Noun Case Extractor with Articles")
sentence = st.text_area("Enter a sentence to translate into German and extract nouns with cases:", height=150)
if st.button("Translate and Extract Nouns"):
    if sentence.strip() == "":
        st.warning("Please enter a sentence.")
prompt = f"""
Translate the following sentence into German AND extract all nouns by German grammatical case.
For each noun, include its definite article (der/die/das) or indefinite article as part of the noun, e.g., "der Lehrer".
Make sure the article is the same as how it appears in your given translation, for example: "den Himmel" stays as "den Himmel" and gets put into Akkusativ.
Don't just put them into the list based on their articles, analyze their ACTUAL role in the sentence.
do NOT include ich, du, wir,.... ,and also names.
do NOT extract the adjectives, ONLY the noun itself and article.

Sentence: "{sentence}"

Return ONLY valid JSON.
NO explanations.
NO markdown.
NO backticks.

Use this EXACT structure:

{{
    "translation": "",
    "Nominativ": [],
    "Akkusativ": [],
    "Dativ": [],
    "Genitiv": [],
    "maskulin" : 0,
    "neutral" : 0,
    "feminin" : 0
}}

Now put each extracted noun into the corresponding Dictionary as a List and only add each noun ONCE
and add to the gender counter the noun's gender. For example: if you find "Lehrer" turn "maskuline" from 0 into 1 and so on.
Make sure to add to "maskulin" "neutral" or "feminin" everytime a noun is found, regardless of case.
for example:

Das Pferd trifft einen Hund und sie luden die Katze zur Party ein.

    "translation": "Das Pferd trifft einen Hund und sie luden die Katze zur Party ein.", 
    "Nominativ": [ "Das Pferd" ], 
    "Akkusativ": [ "einen Hund", "die Katze" ], 
    "Dativ": [ "zur Party" ], 
    "Genitiv": [], 
    "maskulin": 1, "neutral": 1, "feminin": 2 

this is because Hund is maskulin, Katze is feminin, Pferd is neutral, Party is feminin
"""

response = model.generate_content(prompt, generation_config=generation_config)

#ts cuz dumbass ai never gives the same response for some reason
raw = response.text.strip().replace("```json", "").replace("```", "")

try:
    data = json.loads(raw)
except json.JSONDecodeError:
    print("JSON parsing failed. Raw response:")
    print(raw)
    data = {}

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


st.subheader("German Translation")
st.write(translation)
st.subheader("Noun Case DataFrame (with articles)")
st.dataframe(df.sort_index())
fig = px.pie(sizes, names=labels, values=sizes, title="Pie Chart of German Genders")
st.plotly_chart(fig)