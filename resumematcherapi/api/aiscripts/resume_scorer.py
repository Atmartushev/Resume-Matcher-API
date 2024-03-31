import openai
from PyPDF2 import PdfReader 


class ResumeScorer:

    def __init__(self):
        self.default_rubric = " 40 points for experience, 20 points for skills, 20 points for education, 20 points for misc"

    def extract_text_from_pdf(self, pdf_path):
        try:
            reader = PdfReader(pdf_path)
            return reader.pages[0].extract_text()
        except Exception as e:
            return f"Failed to read PDF: {str(e)}"

    def score_resume(self, resume_path, job_description, rubric):
        try:
            resume_path = self.extract_text_from_pdf(resume_path) if resume_path.endswith('.pdf') else open(resume_path, 'r').read()

            prompt = f"You are a job matcher. I will give you a job description and a resumes and you will give it a score 1-100 and explain why.Here is the rubric: {rubric}  The job description is: {job_description}. The resume is: {resume_path}. Make sure to include the name of the resume aswell"

            client = openai.OpenAI(api_key="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")
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )

            return response.choices[0].message.content
        except Exception as e:
            return f"Failed to score resume: {str(e)}"
