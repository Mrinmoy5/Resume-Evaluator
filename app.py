from dotenv import load_dotenv
import streamlit as st
import os
import fitz  # PyMuPDF for text extraction from PDFs
import base64
import google.generativeai as genai

# Load environment variables
load_dotenv()

def configure_genai():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise EnvironmentError("GOOGLE_API_KEY is not set in environment variables.")
    genai.configure(api_key=api_key)

def get_gemini_response(input_text, pdf_content, prompt):
    # Send job description, resume, and prompt to the Gemini model
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content([input_text, pdf_content, prompt])
        return response.text
    except Exception as e:
        return f"Error generating response: {e}"

def extract_text_from_pdf(upload_file):
    # Extract text from uploaded PDF using PyMuPDF
    try:
        pdf_reader = fitz.open(stream=upload_file.read(), filetype="pdf")
        text_content = ""
        for page in pdf_reader:
            text_content += page.get_text()
        pdf_reader.close()
        if not text_content.strip():
            raise ValueError("The uploaded PDF contains no extractable text.")
        return text_content
    except Exception as e:
        raise ValueError(f"Error extracting text from PDF: {e}")

# Streamlit app
st.set_page_config(page_title="ATS Resume Expert", layout="wide")
st.header("ATS Tracking System")

configure_genai()

# Input fields
input_text = st.text_area("Job Description:", height=200)
uploaded_file = st.file_uploader("Upload your resume (PDF only)", type=["pdf"])
if uploaded_file:
    st.write("Resume uploaded successfully.")

submit1 = st.button("Evaluate Resume")
submit3 = st.button("Percentage Match")

input_prompt1 = """
   You are an experienced HR with Tech Experience in the field of Data Science,
   Full Stack Development, Big Data Engineering, DevOps, and Data Analysis.
   Your task is to review the provided resume against the job description for this profile.
   Please share your professional evaluation on whether the candidate's profile aligns
   with the job description and highlight the strengths and weaknesses of the applicant 
   in relation to the specified job role.
"""

input_prompt3 = """
   You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of 
   Data Science, Full Stack Development, Big Data Engineering, DevOps, and Data Analysis.
   Your task is to evaluate the resume against the provided job description. Provide the 
   percentage match of the resume to the job description. First, the output should be the 
   percentage, followed by keywords that are missing.
"""

if submit1:
    if uploaded_file:
        try:
            pdf_content = extract_text_from_pdf(uploaded_file)
            response = get_gemini_response(input_text, pdf_content, input_prompt1)
            st.subheader("Evaluation Response:")
            st.write(response)
        except Exception as e:
            st.error(f"Error processing resume: {e}")
    else:
        st.warning("Please upload a resume.")

if submit3:
    if uploaded_file:
        try:
            pdf_content = extract_text_from_pdf(uploaded_file)
            response = get_gemini_response(input_text, pdf_content, input_prompt3)
            st.subheader("Percentage Match:")
            st.write(response)
        except Exception as e:
            st.error(f"Error processing resume: {e}")
    else:
        st.warning("Please upload a resume.")
