"""
-- Created by: Ashok Kumar Pant
-- Email: asokpant@gmail.com
-- Created on: 03/04/2025
"""

import requests
import streamlit as st

from webapp.api_config import APIConfig

st.title("Recommendation System")

user_id = st.text_input("Enter a user_id:")
if st.button("Get Recommendation"):
    if user_id:
        url = f"{APIConfig.API_BASE_URL}/ml/recommend"
        response = requests.get(url, params={"user_id": user_id, "top_n": 10})
        data = response.json()
        if response.status_code == 200:
            st.write(f"Recommendation: {data["recommendations"]}")
        else:
            st.write(f"Error: {data["error_code"]} - {data["message"]}")
    else:
        st.write("Please enter a user_id.")
