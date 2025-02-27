import streamlit as st
import google.generativeai as genai
import re
import os

# Secure API Key Management
JOURNEY_API_KEY = "AIzaSyBRHQUx1rdAKL8MkOxgE1oyg-S1lvcp1WE"  # Store API key as an environment variable

if not JOURNEY_API_KEY:
    st.error("API Key is missing! Please set the GOOGLE_API_KEY environment variable.")
else:
    genai.configure(api_key=JOURNEY_API_KEY)

    # Use a valid Gemini model
    MODEL_NAME = "gemini-1.5-pro-latest"  # Change this based on available models

    # Load AI Model
    model = genai.GenerativeModel(MODEL_NAME)

    # Function to get journey recommendations
    def get_journey_recommendations(origin, destination, distance):
        prompt = f"""
        You are a journey planner. Provide travel options between {origin} and {destination}, 
        considering a distance of approximately {distance} kilometers. Include the following modes 
        of transport: car, train, bus, and flight. For each mode, provide: 
        1. Estimated cost in USD. 
        2. Approximate travel time. 
        3. Pros and cons of each mode. 
        4. Additional travel tips and best time to book. 
        Format the response in a structured and user-friendly format.
        """
        try:
            response = model.generate_content(prompt)
            return response.text if hasattr(response, "text") else str(response)
        except Exception as e:
            return f"Error fetching journey recommendations: {e}"

    # Streamlit App UI
    st.title("Journey Planner 🚆✈️🚗")
    st.write("Plan your journey with AI-powered recommendations!")

    # Input Fields
    col1, col2, col3 = st.columns(3)
    with col1:
        origin = st.text_input("Enter Origin City:")
    with col2:
        destination = st.text_input("Enter Destination City:")
    with col3:
        distance = st.number_input("Enter Distance (km):", min_value=1)

    # Button to Generate Recommendations
    st.markdown("---")
    if st.button("Get Journey Recommendations", type="primary"):
        if origin and destination and distance:
            with st.spinner("Fetching journey options..."):
                recommendations = get_journey_recommendations(origin, destination, distance)
                
                if "Error" in recommendations:
                    st.error(recommendations)
                else:
                    st.success("Journey Recommendations:")
                    st.write(recommendations)
                    
                    # Display additional journey tips
                    st.markdown("---")
                    st.subheader("Additional Journey Tips")
                    st.write("✅ Book early to get the best prices.")
                    st.write("✅ Compare multiple journey platforms for better deals.")
                    st.write("✅ Consider layovers to reduce flight costs.")
                    st.write("✅ Check luggage policies before booking.")
        else:
            st.warning("Please enter origin, destination, and distance.")
