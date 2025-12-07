import streamlit as st
import pandas as pd
import numpy as np
import google.generativeai as genai
import os
import json

api_key = st.sidebar.text_input("Enter your Google Generative AI API Key:", type="password")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.5-flash-lite")

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
Also include ich, du, wir,.... ,and also names.

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
    "Genitiv": []
}}

Now put each extracted noun into the corresponding Dictionary as a List and only add each noun ONCE
"""

response = model.generate_content(prompt)

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


print("\nGerman translation:")
print(translation)

print("\nNoun Case DataFrame (with articles):")
print(df)

st.subheader("German Translation")
st.write(translation)
st.subheader("Noun Case DataFrame (with articles)")
st.dataframe(df.sort_index())