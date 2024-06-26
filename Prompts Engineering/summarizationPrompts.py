# -*- coding: utf-8 -*-
"""Indepth_Summarization.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1CbLElDlzFvRN8prO5iBtF35tGbRcphgZ
"""

from google.colab import files

uploaded = files.upload()

import pandas as pd
df = pd.read_csv("bills_cleaned - bills_cleaned.csv")

df.columns

from openai import OpenAI
import requests

#Last Semester prompts

Prompt1 = """I want you to act as a text summarizer and provide a concise summary of the bill separated by ####. Summarize the text so {level} can understand. Your summary should be no more than 4 sentences. Do not include your opinions or interpretations and do not make up any false information. Also, I want you to define the main topic for this bill. For example, Topic: Bills about injustice.

####
{context}
####"""

Prompt2 = """I want a summarizer that reads and summarizes legal bills and legislation. I want the summary to not be vague and include the general amendments, area the legislation is affecting, the purpose, the town/city it is affecting, etc. Based on the bill text {context} given, please create a concise and easy-to-understand summary with the relevant key points."""

Prompt3 = """You are an experienced attorney in Massachusetts. Write a concise summary of the bill separated by #### so {level} can understand. Do not make up false information. Include the general amendments, area the legislation is affecting, the purpose, the town and city it is affecting.

####
{context}
####"""

#
template = """Your task is to generate a concise summary of a bill from the Massachusetts legislature. Make sure to capture the main idea of the bill.

Summarize the bill below, delimited by triple backticks, and summarize in a way so {level} can understand.

These are the information bill: {context} tags: #### {schema} ####

Provide your summary in a consistent style. Summary: your summary

Category: choose one category from the list of categories, delimited by ####, that is relevant to the summary.

Next, after you select a category, identify tags that are relevant to your summary. Do not make up any false information."""

#Introducing levels to summurization
# Prompt 1-3 provides summaries that can be used in the context section but for the sake of testing they are removed

#i.e
template = """Your task is to generate a concise summary of a bill from the Massachusetts legislature. Make sure to capture the main idea of the bill.

Summarize the bill below, delimited by triple backticks, and summarize in a way so {level} can understand.

These are the information bill: {context}

Provide your summary in a consistent style. Summary: your summary

Category: choose one category from the list of categories, delimited by ####, that is relevant to the summary.

Next, after you select a category, identify tags that are relevant to your summary. Do not make up any false information."""


Level = {
    "elementaryschoolsummary": """Your task is to generate a concise summary of a bill from the Massachusetts legislature. Make sure to capture the main idea of the bill.
    Summarize a Massachusetts legislative bill using simple language. Write the main idea of the bill below, separated by triple backticks.
    Ensure it's easy to understand for a fourth-grade student with simple sentences and basic vocabulary used to explain concepts.
    . Keep your writing style clear and straightforward. Do not make up any false information.""",

    "highschool_summary": """Your task is to generate a concise summary of a bill from the Massachusetts legislature. Make sure to capture the main idea of the bill.
    Summarize a Massachusetts legislative bill using simple language. Write the main idea of the bill below, separated by triple backticks.
    Ensure it's easy to understand for a high school student. Keep your writing style clear and straightforward. Do not make up any false information.""",

    "college_summary": """Your task is to generate a concise summary of a bill from the Massachusetts legislature. Make sure to capture the main idea of the bill.
    Summarize a Massachusetts legislative bill using simple language. Write the main idea of the bill below, separated by triple backticks.
    Ensure it's easy to understand for a non-law college student. Keep your writing style clear and straightforward. Do not make up any false information.""",

    "general_summary": """Your task is to generate a concise summary of a bill from the Massachusetts legislature. Make sure to capture the main idea of the bill.
    Summarize a Massachusetts legislative bill using simple language. Write the main idea of the bill below, separated by triple backticks.
    Ensure it's easy to understand for the general public. The generated summary should use clear, straightforward language, and any necessary terminology is explained in layman's terms.
    Do not make up any false information.""",

    "lawyer_summary": """Your task is to generate a concise summary of a bill from the Massachusetts legislature. Make sure to capture the main idea of the bill.
    Summarize a Massachusetts legislative bill using simple language. Write the main idea of the bill below, separated by triple backticks.
    Ensure it's easy to understand for a legal professional that has a professional level of understanding of the law. Keep your writing style clear and straightforward.
    Do not make up any false information."""
}

# filled_template = template.format(context=context_example, level=level, schema=schema_example)

# # Print the filled template (or any other prompt you wish to use)
# print(filled_template)

testbill1 = str(df['DocumentText'].iloc[0])
print(testbill1)

# Chatgpt API
import requests

api_key = "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"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

# First prompt {elementary summary}
prompt = list(Level.values())[0]
full_prompt = f"{prompt} for this bill: {testbill1}"
data = {
    "model": "gpt-3.5-turbo",
    "messages": [{"role": "user", "content": full_prompt}],
    "temperature": 0.7
}

response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
print(response.json())

#Claude API
import anthropic

client = anthropic.Anthropic(
    api_key="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",
)

prompt = list(Level.values())[0]
full_prompt = f"{prompt} for this bill: {testbill1}"
message_to_claude = [
    {
        "role": "user",
        "content": {
            "type": "text",
            "text": full_prompt
        }
    }
]
message = client.messages.create(
    model="claude-3-sonnet-20240229",
    max_tokens=1000,
    temperature=0,
    system="Respond in plain, easy-to-understand language.",
    messages=message_to_claude
)
print(message.content)



# text summarization chatbot
#https://huggingface.co/Falconsai/text_summarization
x =  list(Level.values())
print( f"{x[0]} for this bill: {testbill1}")

from transformers import pipeline

# Instantiate the pipeline for summarizing
summarizer = pipeline("summarization", model="Falconsai/text_summarization")
a = summarizer(testbill1, max_length=50, min_length=10, do_sample=False)
b = testbill1

print (a)
print(b)