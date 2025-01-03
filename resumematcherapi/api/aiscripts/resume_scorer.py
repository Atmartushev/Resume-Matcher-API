import os
from dotenv import load_dotenv
import openai
from PyPDF2 import PdfReader 

class ResumeScorer:

    def score_resume(self, resume_text, job_description, rubric):
        try:
            load_dotenv()
            prompt = f"You are a job matcher. I will give you a job description and a resumes and you will give it a score out of 100 and make sure is it out of 100 as an int data type, and explain why. The rubric given will be out of 100, SCORE BASED OF THE RUBRIC. If a candidate doesnt match the job description give it a really bad score. Give Score as an int data type. Here is the rubric: {rubric}  The job description is: {job_description}. The resume is: {resume_text}. Make sure to include the name of the resume aswell."

            client = openai.OpenAI(api_key=os.getenv('SECRET_KEY_CHATGPT'))
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )

            return response.choices[0].message.content
        except Exception as e:
            return f"Failed to score resume: {str(e)}"
