import databutton as db
import streamlit as st
import pandas as pd
import re
import openai
import os

# Define the model to use
MODEL_NAME = "gpt-3.5-turbo"

sku_data = pd.read_csv("./sku_data.csv")
country_id_mapping = pd.read_csv("./country_id_mapping.csv")
session_clickstream_data = pd.read_csv("./session_clickstream_data.csv")
customer_data = pd.read_csv("./customer_data.csv")



def handle_openai_query(df):
    """
    Handle the OpenAI query and display the response.

    Parameters:
    - df: list of DataFrames containing the data
    """

    # Create a text area for user input
    query = st.text_area(
        "Enter your Prompt:",
        placeholder="Prompt tips: Use plotting related keywords such as 'Plots' or 'Charts' or 'Subplots'. Prompts must be concise and clear, example 'Bar plot for the first ten rows.'",
        help="""
            How an ideal prompt should look like? *Feel free to copy the format and adapt to your own dataset.*
            
            ```
            - Subplot 1: Line plot of the whole spectra.
            - Subplot 2: Zoom into the spectra in region 1000 and 1200.
            - Subplot 3: Compare the area of whole spectra and zoom spectra as Bar Plot.
            - Subplot 4: Area curve of the zoom spectra.
            ```
            """,
    )

    # If the "Get Answer" button is clicked
    if st.button("Get Answer"):
        # Ensure the query is not empty
        if query and query.strip() != "":
            # Define the prompt content
            prompt_content = f"""
            There are 4 datasets already loaded into dataframes. DO NOT load the data again. Data frames are loaded as:
            sku_data = pd.read_csv("./sku_data.csv")
            country_id_mapping = pd.read_csv("./country_id_mapping.csv")
            session_clickstream_data = pd.read_csv("./session_clickstream_data.csv")
            customer_data = pd.read_csv("./customer_data.csv")

            DO NOT again load the dataframes
            
            The DataFrames has the following columns
            sku_data : {df[0](list)}
            country_id_mapping : {df[1](list)}
            session_clickstream_data : {df[2](list)}
            customer_data : {df[3](list)}


            
            Before plotting, ensure the data is ready:
            1. Check if columns that are supposed to be numeric are recognized as such. If not, attempt to convert them.
            2. Handle NaN values by filling with mean or median.
            
            Use package Pandas and Matplotlib ONLY.
            Provide SINGLE CODE BLOCK with a solution using Pandas and Matplotlib plots in a single figure to address the following query:
            
            {query}

            - USE SINGLE CODE BLOCK with a solution. 
            - Do NOT EXPLAIN the code 
            - DO NOT COMMENT the code. 
            - ALWAYS WRAP UP THE CODE IN A SINGLE CODE BLOCK.
            - The code block must start and end with ```
            
            - Example code format ```code```
        
            - Colors to use for background and axes of the figure : #F0F0F6
            - Try to use the following color palette for coloring the plots : #8f63ee #ced5ce #a27bf6 #3d3b41
            
            """

            # Define the messages for the OpenAI model
            messages = [
                {
                    "role": "system",
                    "content": "You are a helpful Data Visualization assistant who gives a single block without explaining or commenting the code to plot. IF ANYTHING NOT ABOUT THE DATA, JUST politely respond that you don't know.",
                },
                {"role": "user", "content": prompt_content},
            ]

            # Call OpenAI and display the response
            with st.status("📟 *Prompting is the new programming*..."):
                with st.chat_message("assistant", avatar="📊"):
                    botmsg = st.empty()
                    response = []
                    for chunk in openai.ChatCompletion.create(
                        model=MODEL_NAME, messages=messages, stream=True
                    ):
                        text = chunk.choices[0].get("delta", {}).get("content")
                        if text:
                            response.append(text)
                            result = "".join(response).strip()
                            botmsg.write(result)
            execute_openai_code(result, df, query)


def extract_code_from_markdown(md_text):
    """
    Extract Python code from markdown text.

    Parameters:
    - md_text: Markdown text containing the code

    Returns:
    - The extracted Python code
    """
    # Extract code between the delimiters
    code_blocks = re.findall(r"```(python)?(.*?)```", md_text, re.DOTALL)

    # Strip leading and trailing whitespace and join the code blocks
    code = "\n".join([block[1].strip() for block in code_blocks])

    return code

def execute_openai_code(response_text: str, df: pd.DataFrame, query):
    """
    Execute the code provided by OpenAI in the app.

    Parameters:
    - response_text: The response text from OpenAI
    - df: DataFrame containing the data
    - query: The user's query
    """

    # Extract code from the response text
    code = extract_code_from_markdown(response_text)

    # If there's code in the response, try to execute it
    if code:
        try:
            exec(code)
            st.pyplot()
        except Exception as e:
            error_message = str(e)
            st.error(
                f"📟 Apologies, failed to execute the code due to the error: {error_message}"
            )
            st.warning(
                """
                📟 Check the error message and the code executed above to investigate further.

                Pro tips:
                - Tweak your prompts to overcome the error 
                - Use the words 'Plot'/ 'Subplot'
                - Use simpler, concise words
                - Remember, I'm specialized in displaying charts not in conveying information about the dataset
            """
            )
    else:
        st.write(response_text)



# Suppress deprecation warnings related to Pyplot's global use
st.set_option("deprecation.showPyplotGlobalUse", False)


df = [sku_data, country_id_mapping, session_clickstream_data, customer_data]

# Handle the OpenAI query and display results
handle_openai_query(df)