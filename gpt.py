import streamlit as st
from langchain_community.document_loaders import csv_loader
from langchain.indexes import VectorstoreIndexCreator
from langchain_community.llms import openai
from langchain_community.chat_models import ChatOpenAI
from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from langchain_openai import ChatOpenAI, OpenAI
from dotenv import load_dotenv

def main():
    load_dotenv()

    st.set_page_config(page_title="CSV GPT")
    st.header("CSV GPT")

    option = st.selectbox(
        'Select Prompt Difficulty!',
         ('Easy', 'Medium', 'Hard'))

    if option == "Easy":
        st.button(
            "In which month was the most products sold?", use_container_width=False)
    
    elif option == "Medium":
        st.button(
            "What are the most common sizes available for the top-selling products?",use_container_width=False)
        st.button(
            "What is the average spend in the summer vs spring?",use_container_width=False)
        st.button(
            "Identify top customers with high purchases and determine what is their common frequency to buy?",use_container_width=False)
        st.button(
            "What is the most common color amongst the different clothing types?",use_container_width=False)
        
    else:
        st.button(
            "How many products does a customer browse before making a purchase on weekends and holidays vs weekdays?",use_container_width=False)
        st.button(
            "What were the 5 most common product colors sold in Europe in May, June, and July?",use_container_width=False)
        st.button(
            "Are there any trends in product features (texture, color, type) and the session activity (time spent, avg purchases, etc.)?",use_container_width=False)


        

        

    user_prompt = st.text_input("Enter your Prompt")

    agent = create_csv_agent(
    ChatOpenAI(temperature=0, model="gpt-3.5-turbo"),
    ["country_id_mapping.csv", "customer_data.csv", "session_clickstream_data.csv", "sku_data.csv"],
    verbose=True,
    agent_type=AgentType.OPENAI_FUNCTIONS,
    )
    
    if user_prompt is not None and user_prompt != "":
        response = agent.run(user_prompt)
        st.write(response)
         
if __name__ == "__main__":
    main()