from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=250)
    pfp = models.CharField(max_length=500)
    email = models.CharField(max_length=300, unique=True)

class Rubric(models.Model):
    sections = models.TextField()

class Job(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'), 
        ('medium', 'Medium'), 
        ('high', 'High')
    ]

    name = models.CharField(max_length=200)
    jod_description = models.CharField(max_length=10000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rubric = models.ForeignKey(Rubric, on_delete=models.CASCADE)
    date_created = models.DateField(auto_now_add=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='low')

class Candidate(models.Model):
    name = models.CharField(max_length=250, default='Name Not Provided')
    resume = models.FileField(upload_to='resumes/', default='N/A')
    resume_score = models.TextField(default='0')
    resume_score_description = models.TextField(default='N/A')
    contact = models.CharField(max_length=100, default='Contact Not Available')
    job = models.ForeignKey(Job, on_delete=models.CASCADE)