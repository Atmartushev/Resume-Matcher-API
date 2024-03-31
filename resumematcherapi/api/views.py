from django.http import HttpResponseRedirect
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.decorators import api_view
from django.http import JsonResponse
from core.models import *
from .serializers import CandidateSerializer, JobSerializer, UserSerlializer
from .forms import UploadFileForm
from .aiscripts import ResumeScorer, ResumeParser, RubricGenerator

@api_view(['GET'])
def getAllUsers(request):
    users = User.objects.all()
    serializer = UserSerlializer(users, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getUser(request, id):
    try:
        user = User.objects.get(id = id)
        serializer = UserSerlializer(user)
        return Response(serializer.data)
    except:
        return Response({"message": "User not found"}, status=404)
    
@api_view(['GET'])
def getUserByEmail(request, email):
    try:
        user = User.objects.get(email = email)
        serializer = UserSerlializer(user)
        return Response(serializer.data)
    except:
        return Response({"message": "User not found"}, status=404)

@api_view(['POST'])
def addUser(request):
    serializer = UserSerlializer(data=request.data)
    if serializer.is_valid():
        # Check if user already exists
        if User.objects.filter(email=serializer.validated_data['email']).exists():
            return Response({"message": "User already exists"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        serializer.save()
    else:
        return Response({"message": "Invalid user data"}, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.data)

@api_view(['GET'])
def getAllJobsByUserId(request, user_id):
    try:
        # Get all jobs for the given user_id
        jobs = Job.objects.filter(user_id=user_id)
        
        # Serialize the job data
        serializer = JobSerializer(jobs, many=True)
        
        # Return the serialized job data
        return Response(serializer.data)
    except:
        # Return an error response if something goes wrong
        return Response({"message": "An error occurred while retrieving jobs"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def getAllCandidatesByJobId(request, job_id):
    try:
        # Get all candidates for the given job_id
        candidates = Candidate.objects.filter(job_id=job_id)
        
        # Serialize the candidate data
        serializer = CandidateSerializer(candidates, many=True)
        
        # Return the serialized candidate data
        return Response(serializer.data)
    except:
        # Return an error response if something goes wrong
        return Response({"message": "An error occurred while retrieving candidates"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def add_candidate(request, job_id):
    attributes = ["Name", "Email", "Phone Number", "Score"]
    job = Job.objects.get(id=job_id)
    form = UploadFileForm(request.POST, request.FILES)
    if form.is_valid():
        job_rubric = RubricGenerator.generate_rubric(job.description)

        # Parse the resume and get the candidate data
        candidate_score = ResumeScorer.score_resume(request.FILES['file'], job.description, job_rubric)

        candidate_data = ResumeParser.parse_resume(candidate_score, attributes)

        # You may still want to save the candidate or log the score here
        # Depending on your application's requirements
        candidate = Candidate(name=candidate_data['Name'], resume=request.FILES['file'], resume_score=candidate_data['Score'], contact=candidate_data['Email'], job=job)
        candidate.save()

        # Return the score in a JSON response
        return JsonResponse({'score': candidate_data['Score']})
    else:
        # Return an error message or invalid form notification as JSON
        return JsonResponse({'error': 'Invalid form data'}, status=400)

