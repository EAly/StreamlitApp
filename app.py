# app.py
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

# UI setup
st.set_page_config(page_title="MBSE & Mission Engineering GPT", layout="wide")
st.title("MBSE & Mission Engineering Assistant")

# Load your OpenAI API Key from secrets (you'll define this later in deployment)
try:
    openai_api_key = st.secrets["OPENAI_API_KEY"]
except Exception:
    openai_api_key = st.text_input("Enter your OpenAI API key to continue", type="password")
    if not openai_api_key:
        st.warning("Please enter your OpenAI API key.")
        st.stop()

# Load LLM
llm = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=openai_api_key, temperature=0)

# Custom prompt (can be adjusted with more MBSE context later)
template = PromptTemplate(
    input_variables=["question"],
    template=(
        "You are an expert in Model-Based Systems Engineering (MBSE) and Mission Engineering. "
        "Answer the following question with reference to established systems thinking, modeling practices, and mission engineering principles.\n\n"
        "Question: {question}"
    ),
)

# User input
question = st.text_area("Ask your MBSE question (e.g., about requirements, Capella, modeling levels, etc.):")

if question:
    with st.spinner("Thinking..."):
        prompt = template.format(question=question)
        response = llm.invoke(prompt)
        st.success("Response:")
        st.write(response.content)
