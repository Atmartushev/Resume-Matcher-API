from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=50)
    pfp = models.CharField(max_length=400)
    email = models.CharField(max_length=100)

class Rubric(models.Model):
    sections = models.TextField()

class Job(models.Model):
    name = models.CharField(max_length=200)
    jod_description = models.CharField(max_length=2000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rubric = models.ForeignKey(Rubric, on_delete=models.CASCADE)

class Candidate(models.Model):
    name = models.CharField(max_length=50, default='Name Not Provided')
    resume = models.FileField(upload_to='resumes/', default='N/A')
    resume_score = models.TextField(default='0')
    resume_score_description = models.TextField(default='N/A')
    contact = models.CharField(max_length=50, default='Contact Not Available')
    job = models.ForeignKey(Job, on_delete=models.CASCADE)