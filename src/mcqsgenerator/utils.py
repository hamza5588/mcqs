import os
import PyPDF2
import json
import traceback
import re


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
        return file.read().decode("utf-8")
    
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
        return mcqs_text
    else:
        print("MCQs part not found in the text.")
        return ""
