import os
import openai
from PyPDF2 import PdfReader 
import io


class RubricGenerator:



    def create_rubric(self, job_description):

        prompt = """Using the following job description, create a detailed rubric for evaluating candidates' suitability for the position. The rubric should be out of a total of 100 points, with each attribute categorized under specific criteria derived from the job description. Each criterion should have five levels of scoring, ranging from 'Excellent' to 'Poor'. For each level, provide a descriptive and detailed grading that aligns with expectations set in the job description, where meeting the job requirements corresponds to an 'Average' score. Ensure the descriptions for each scoring level are specific, actionable, and tied directly to the job requirements and duties. Break down the total points across the different criteria in a balanced manner that reflects the priorities and importance of each attribute as suggested by the job description.
                    Instructions for ChatGPT:
                    Analyze the Job Description: Begin by carefully reading the job description provided. Identify the key qualifications, skills, and responsibilities listed.
                    Define Criteria: Based on your analysis, define distinct criteria for the rubric. These could include technical skills, soft skills, experience, educational background, and specific responsibilities or achievements mentioned in the job description.
                    Allocate Points: Distribute a total of 100 points across these criteria, assigning more points to areas emphasized as more critical or requiring higher expertise in the job description.
                    Create Scoring Levels: For each criterion, develop five scoring levels Excellent, Good, Average, Below Average, and Poor. Each level should have a point range (e.g., Excellent: 90-100"%" of the points available for that criterion).
                    Detail Each Level: Provide specific, detailed descriptions for what constitutes each scoring level, using language and expectations directly from the job description. For example, if a job requires excellent communication skills, describe what excellent, good, average, below average, and poor communication would look like in the context of this job's duties.
                    Justify Point Allocations: Briefly explain why you've assigned the point values to each criterion and level, referencing the job description's emphasis on certain qualifications or responsibilities.
                    Finalize the Rubric: Conclude with a summary of the rubric, ensuring it is clear, concise, and ready for use in evaluating job candidates. Ensure to have points for each grade aswell. The total points should be out of 100"""

        prompt2 = f"this is the job description: {job_description}. Make sure you actually have a job description. If there is an error report that and do not create a Rubric. Return in Json format"

        client = openai.OpenAI(api_key="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")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt + prompt2}]
        )

        return response.choices[0].message.content
    
    def generate_rubric(self, job_description):
        try:
            response = self.create_rubric(job_description)
            return response
        except Exception as e:
            return f"Failed to generate rubric: {str(e)}"