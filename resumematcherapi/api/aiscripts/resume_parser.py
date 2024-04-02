import gradio as gr
import openai
import os
import pandas as pd
from PyPDF2 import PdfReader 
import re 
import json
import io

class ResumeParser:

    def __init__(self):
        self.api_key = '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'
        self.client = openai.OpenAI(api_key=self.api_key)


    def parse_resume(self, resume_text, attributes):
        """
        Parses the resume file using ChatGPT based on selected attributes.

        Args:
        - resume_file: The uploaded resume file.
        - attributes: A list of attributes to extract from the resume.

        Returns:
        A dictionary with attributes and their values extracted from the resume.
        """
        # Ensure the PDF file is readable
        # Create the prompt for ChatGPT
        attributes_list = "[" + ', '.join(attributes) + "]"
        prompt = self.construct_prompt(attributes_list, resume_text)
        
        # Query OpenAI's ChatGPT with the prompt
        client = openai.OpenAI(api_key="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")
        try:
            # Adjusted call for the new OpenAI API
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
            messages=
            [
                {"role": "system", "content": "You are a resume parser."},
                {"role": "user", "content": prompt}
                ]  ,
                temperature=0,
                max_tokens=1024,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0,
                stop=None  # You might need to set stop sequences depending on your prompt structure
            )

            # Parsing the response according to the new API response structure
            parsed_response = response.choices[0].message.content


            # Convert the parsed response to a dictionary (implement this logic based on your expected response format)
            parsed_output = self.parse_chatgpt_response(parsed_response, attributes)
        except Exception as e:
            parsed_output = {"error": f"Failed to parse response: {str(e)}"}

        return parsed_output

    def parse_chatgpt_response(self, response_text, attributes):
        """
        Parses the text response from ChatGPT into a dictionary based on the specified attributes.

        Args:
        - response_text: The text response from ChatGPT.
        - attributes: A list of attributes that the user wants to extract from the resume.

        Returns:
        A dictionary with the specified attributes as keys and their parsed values.
        """
        # Initialize an empty dictionary to hold the parsed attributes
        parsed_attributes = json.loads(response_text)

        # for attribute in attributes:
        #     # Construct a regex pattern to capture the value after the attribute
        #     # Adjust the pattern based on how ChatGPT formats the response
        #     pattern = f"{attribute}\s*:\s*(.+)"
        #     match = re.search(pattern, response_text, re.IGNORECASE)

        #     if match:
        #         # Add the attribute and its value to the dictionary
        #         parsed_attributes[attribute] = match.group(1).strip()

        return parsed_attributes

    def construct_prompt(self, attributes_list, resume_text):
        prompt = f"You are a resume parser. Please search for and display the following attributes in the format of a python dictionary for each attribute in the list of attributes selected by the client, given here: {attributes_list}. Emails will most likely be in linked together with @ formats so make sure to look especially close for those. \n\nResume:\n{resume_text}"
        return prompt

