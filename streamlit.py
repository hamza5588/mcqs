import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
import streamlit as st
from langchain.callbacks import get_openai_callback
from src.mcqsgenerator.mcqs import generate_evaluate_chain
from src.mcqsgenerator.logger import logging
from fpdf import FPDF
import os
import PyPDF2
import base64
import json
import traceback
import re


 # take environment variables from .env.







def read_file(file):
    if file.name.endswith(".pdf"):
        try:
            pdf_reader=PyPDF2.PdfFileReader(file)
            text=""
            for page in pdf_reader.pages:
                text+=page.extract_text()
            return text
            
        except Exception as e:
            raise Exception("error reading the PDF file")
        
    elif file.name.endswith(".txt"):
        return file.read()
    
    else:
        raise Exception(
            "unsupported file format only pdf and text file suppoted"
            
        )

def extract_mcqs(text):
    # Define the regex pattern to extract the MCQs part
    mcqs_pattern = r"{\s*\"\d+\"\s*:.+}"

    # Search for the MCQs part in the text
    mcqs_match = re.search(mcqs_pattern, text, re.DOTALL)

    if mcqs_match:
        mcqs_text = mcqs_match.group(0)
        mcqs_text=str(mcqs_text)
        mcqs_text = mcqs_text.replace('{"1": {"mcq": "multiple choice question", "options": {"a": "choice here", "b": "choice here", "c": "choice here", "d": "choice here"}, "correct": "correct answer"}, ', '')
        mcqs_text = mcqs_text.replace('"2": {"mcq": "multiple choice question", "options": {"a": "choice here", "b": "choice here", "c": "choice here", "d": "choice here"}, "correct": "correct answer"}, ', '')
        mcqs_text = mcqs_text.replace('"3": {"mcq": "multiple choice question", "options": {"a": "choice here", "b": "choice here", "c": "choice here", "d": "choice here"}, "correct": "correct answer"}}', '')
        mcqs_text = mcqs_text.replace('{"1": {"mcq": "multiple choice question", "options": {"a": "choice here", "b": "choice here", "c": "choice here", "d": "choice here"}, "correct": "correct answer"}, "2": {"mcq": "multiple choice question", "options": {"a": "choice here", "b": "choice here", "c": "choice here", "d": "choice here"}, "correct": "correct answer"}, "3": {"mcq": "multiple choice question", "options": {"a": "choice here", "b": "choice here", "c": "choice here", "d": "choice here"}, "correct": "correct answer"}}', '')
        mcqs_text = mcqs_text.replace('RESPONSE_JSON', '')

        
        return mcqs_text
    else:
        print("MCQs part not found in the text.")
        return ""


RESPONSE_JSON={
    "1": {
        "mcq": "multiple choice question",
        "options": {
            "a": "choice here",
            "b": "choice here",
            "c": "choice here",
            "d": "choice here",
        },
        "correct": "correct answer",
    },
    "2": {
        "mcq": "multiple choice question",
        "options": {
            "a": "choice here",
            "b": "choice here",
            "c": "choice here",
            "d": "choice here",
        },
        "correct": "correct answer",
    },
    "3": {
        "mcq": "multiple choice question",
        "options": {
            "a": "choice here",
            "b": "choice here",
            "c": "choice here",
            "d": "choice here",
        },
        "correct": "correct answer",
    },
}


#creating a title for the app
st.title("MCQs Creator Application with LangChain 🦜⛓️")


with st.form("user input"):
    uploaded_file=st.file_uploader("upload pdf or text")

    mcq_count=st.number_input("no of mcq's", min_value=3, max_value=50)

    subject=st.text_input("Insert Subject",max_chars=20)

    tone=st.text_input("Complexity Level Of Questions", max_chars=20, placeholder="Simple")

    button=st.form_submit_button("Create MCQs")

    if button and uploaded_file is not None and mcq_count and subject and tone:
        with st.spinner("loading..."):
            try:
                # with open(uploaded_file, 'r') as file:
                #     TEXT = file.read()
                text=read_file(uploaded_file)
                # text=uploaded_file.read()
                print("it is ",uploaded_file)
                #Count tokens and the cost of API call
                
                response=generate_evaluate_chain(
                    {
                     
                        "text": text,
                        "number": mcq_count,
                        "subject":subject,
                        "tone": tone,
                        "response_json": json.dumps(RESPONSE_JSON)
                          },
                    )
                

            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
                st.error("Error")

            else:
              
                if isinstance(response, dict):
              
                    #Extract the quiz data from the response
                    quiz=response.get("quiz")
                    if quiz is not None:
                        mcqspart=extract_mcqs(quiz)
                        mcqspart=str(mcqspart)
                        # st.write(mcqspart)
                        if mcqspart is not None:
                            mcqs_part = mcqspart.replace('{"1": {"mcq": "multiple choice question", "options": {"a": "choice here", "b": "choice here", "c": "choice here", "d": "choice here"}, "correct": "correct answer"}, ', '')
                            mcqs_part = mcqspart.replace('"2": {"mcq": "multiple choice question", "options": {"a": "choice here", "b": "choice here", "c": "choice here", "d": "choice here"}, "correct": "correct answer"}, ', '')
                            mcqs_part = mcqspart.replace('"3": {"mcq": "multiple choice question", "options": {"a": "choice here", "b": "choice here", "c": "choice here", "d": "choice here"}, "correct": "correct answer"}}', '')
                            mcqs_part = mcqspart.replace('{"1": {"mcq": "multiple choice question", "options": {"a": "choice here", "b": "choice here", "c": "choice here", "d": "choice here"}, "correct": "correct answer"}, "2": {"mcq": "multiple choice question", "options": {"a": "choice here", "b": "choice here", "c": "choice here", "d": "choice here"}, "correct": "correct answer"}, "3": {"mcq": "multiple choice question", "options": {"a": "choice here", "b": "choice here", "c": "choice here", "d": "choice here"}, "correct": "correct answer"}}', '')



                            mcqs_part = mcqspart.replace('```', '')
                            mcqs_part=eval(mcqs_part)
                            
                            mcqs = mcqs_part
                            pdf = FPDF()
                            pdf.set_auto_page_break(auto=True, margin=15)
                            pdf.add_page()

                            pdf.set_font("Arial", size=12)

                            for key, value in mcqs.items():
                                mcq = value["mcq"]
                                options = value["options"]
                                correct_option = value["correct"]

                                pdf.cell(0, 10, f"{key}. {mcq}", ln=True)

                                for option, text in options.items():
                                    pdf.cell(0, 10, f"{option}) {text}", ln=True)

                                pdf.cell(0, 10, f"Correct Answer: {correct_option.upper()}", ln=True)
                                pdf.cell(0, 10, "", ln=True)  # Add a blank line between questions
                            

                            pdf_bytes = pdf.output(dest="S").encode("latin1")

                            pdf_base64 = base64.b64encode(pdf_bytes).decode('utf-8')


                            pdf_display = f'<embed src="data:application/pdf;base64,{pdf_base64}" width="700" height="1000" type="application/pdf">'
                            st.markdown(pdf_display, unsafe_allow_html=True)

                      


                            pdf.output("MCQs_without_colorgenerator.pdf")
                        else:
                            st.error("Error in the pdf data")
                            

                else:
                    print(type(response))
                    # st.write(response)

if button and uploaded_file is not None and mcq_count and subject and tone:
    st.download_button(
        label="Download PDF",
        data=pdf_bytes,
        file_name="MCQs_generated.pdf",
        mime="application/pdf"
    )