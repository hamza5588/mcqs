import os
import json
import pandas as pd
import traceback
from dotenv import load_dotenv
from langchain import HuggingFaceHub
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
import PyPDF2


load_dotenv()  # take environment variables from .env.
KEY=os.getenv("huggingfacehub_api_token")

repo_id = "mistralai/Mixtral-8x7B-Instruct-v0.1"
llm = HuggingFaceHub(huggingfacehub_api_token=KEY, 
                     repo_id=repo_id, 
                     model_kwargs={"temperature":0.8, "max_new_tokens":5000})


RESPONSE_JSON = {
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

TEMPLATE="""
Text:{text}
You are an expert MCQ maker. Given the above text, it is your job to \
create a quiz  of {number} multiple choice questions for {subject} students in {tone} tone. 
Make sure the questions are not repeated and check all the questions to be conforming the text as well.
Make sure to format your response like  RESPONSE_JSON below   and use it as a guide do not repeat my prompt in your responce. \
Ensure to make {number} MCQs
### RESPONSE_JSON
{response_json}

"""
quiz_generation_prompt = PromptTemplate(
    input_variables=["text", "number", "subject", "tone", "response_json"],
    template=TEMPLATE
    )

quiz_chain=LLMChain(llm=llm, prompt=quiz_generation_prompt, output_key="quiz", verbose=True)

TEMPLATE2="""
You are an expert english grammarian and writer. Given a Multiple Choice Quiz for {subject} students.\
You need to evaluate the complexity of the question and give a complete analysis of the quiz.\ check whether it generate  {number} mcqs\
and also check it give the proper responce \
if the quiz is not at per with the cognitive and analytical abilities of the students,\
update the quiz until whether it matches the exact mcqs {number} which provide in the prompt questions and do not repeat the prompt that the user has give and change the tone  such that it perfectly fits the student abilities
Quiz_MCQs:
{quiz}

Check from an expert English Writer of the above quiz:
"""

quiz_evaluation_prompt=PromptTemplate(input_variables=["subject", "quiz"], template=TEMPLATE)

review_chain=LLMChain(llm=llm, prompt=quiz_evaluation_prompt, output_key="review", verbose=True)

generate_evaluate_chain=SequentialChain(chains=[quiz_chain, review_chain], input_variables=["text", "number", "subject", "tone", "response_json"],
                                        output_variables=["quiz", "review"], verbose=True,)
# file_path=r"C:\Users\PMLS\Desktop\New folder (16)\data.txt"

# with open(file_path, 'r') as file:
#     TEXT = file.read()


# NUMBER=20
# SUBJECT="english"
# TONE="difficult"

# response=generate_evaluate_chain(
#         {
#             "text": TEXT,
#             "number": NUMBER,
#             "subject":SUBJECT,
#             "tone": TONE,
#             "response_json": json.dumps(RESPONSE_JSON)
#         }
# )


