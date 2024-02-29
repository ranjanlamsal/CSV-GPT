import streamlit as st
import pandas as pd
from pandasai import SmartDatalake
from datetime import datetime
from pandasai.llm import OpenAI
from dotenv import load_dotenv

def main():

    # Load environment variables from .env file
    load_dotenv()

    #OpenAI language learning model
    llm = OpenAI(api_token="your-api-key")

    #Importing Necessary Dataframes
    sku_data = pd.read_csv("./sku_data.csv")
    country_id_mapping = pd.read_csv("./country_id_mapping.csv")
    session_clickstream_data = pd.read_csv("./session_clickstream_data.csv")
    customer_data = pd.read_csv("./customer_data.csv")

    #For Multiple Dataset Using DataLake
    df = SmartDatalake([sku_data, country_id_mapping, session_clickstream_data, customer_data], config={"llm": llm})

    #Streamlit page configuration
    st.set_page_config(page_title="CSV GPT")
    st.header("CSV GPT")

    option = st.selectbox(
        'Select Prompt Difficulty!',
         ('Easy', 'Medium', 'Hard'))

    if option == "Easy":
        if st.button(
            "In which month was the most products sold?", use_container_width=False):
            response = df.chat("In Which month was the most product sold")
            st.write(response)

    
    elif option == "Medium":
        if st.button(
            "What are the most common sizes available for the top-selling products?",use_container_width=False):
            response = df.chat("What are the most common sizes available for the top-selling products")
            st.write(response)

        if st.button(
            "What is the average spend in the summer vs spring?",use_container_width=False):
            response = df.chat("What is the average spend in the summer vs spring")
            st.write(response)

        if st.button(
            "Identify top customers with high purchases and determine what is their common frequency to buy?",use_container_width=False):
            response = df.chat("Identify top customers with high purchases and determine what is their common frequency to buy")
            st.write(response)

        if st.button(
            "What is the most common color amongst the different clothing types?",use_container_width=False):
            response = df.chat("What is the most common color amongst the different clothing types")
            st.write(response)

    else:
        if st.button(
            "How many products does a customer browse before making a purchase on weekends and holidays vs weekdays?",use_container_width=False):
            response = df.chat("How many products does a customer browse before making a purchase on weekends and holidays vs weekdays")

        if st.button(
            "What were the 5 most common product colors sold in Europe in May, June, and July?",use_container_width=False):
            response = df.chat("What were the 5 most common product colors sold in Europe in May, June, and July")
            st.write(response)

        if st.button(
            "Are there any trends in product features (texture, color, type) and the session activity (time spent, avg purchases, etc.)?",use_container_width=False):
            response = df.chat("Are there any trends in product features (texture, color, type) and the session activity (time spent, avg purchases, etc.)")
            st.write(response)

        

    user_prompt = st.text_input("Enter your Prompt")
    response = df.chat(user_prompt)
    st.write(response)



if __name__ == "__main__":
    main()