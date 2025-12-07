import streamlit as st
import pandas as pd
import numpy as np
import google.generativeai as genai
import os
import json

st.title("Simple Data Analysis App")

api_key = "AIzaSyBEwVeQhjuPvUKBF2GprB3xCosVzmspgxY"

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.5-flash-lite")

prompt = "Explain the difference between a Generative model and a Discriminative model in simple terms."

response = model.generate_content(prompt)
print(response.text)