from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=50)
    pfp = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    email = models.CharField(max_length=100)

class Rubric(models.Model):
    sections = models.CharField(max_length=400)

class Job(models.Model):
    name = models.CharField(max_length=200)
    jod_description = models.CharField(max_length=2000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rubric = models.ForeignKey(Rubric, on_delete=models.CASCADE)

class Candidate(models.Model):
    name = models.CharField(max_length=50)
    resume = models.CharField(max_length=2000)
    rubric_score = models.FloatField()
    contact = models.CharField(max_length=50)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)