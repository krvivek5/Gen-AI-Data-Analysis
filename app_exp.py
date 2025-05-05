import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf

from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
st.set_page_config(page_title="Chat with PDF", page_icon=":book:", layout="wide")

st.title("Chat with PDF :book:")
st.write("Upload a PDF file and ask questions about its content.")
st.write("Powered by Google Generative AI")

st.write("Note: This app is in beta. Please provide feedback on your experience.")
st.write("Disclaimer: This app is for educational purposes only. Please do not upload sensitive or confidential documents.")

# Gemini Pro Response
def get_gemini_response(prompt):
    try:
        model=genai.GenerativeModel("gemini-1.5-flash") # Ensure this is the correct model name from the list
        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        st.error(f"Error: {e}")
        return None
    
# PDF Upload
uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

if uploaded_file is not None:
    # Read PDF file
    pdf_reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    
    # Display PDF content
    st.subheader("PDF Content")
    st.write(text[:1000] + "...")  # Display first 1000 characters

    # User question input
    user_question = st.text_input("Ask a question about the PDF content:")

    if st.button("Get Answer"):
        if user_question:
            with st.spinner("Generating response..."):
                response = get_gemini_response(user_question)
                if response:
                    st.subheader("Response")
                    st.write(response)
                else:
                    st.error("Failed to get a response. Please try again.")
        else:
            st.error("Please enter a question.")

    # Clear button
    if st.button("Clear"):
        st.rerun()

