from io import BytesIO
from django.http import HttpResponseRedirect
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.decorators import api_view
from django.http import JsonResponse
from core.models import *
from .serializers import CandidateSerializer, JobSerializer, RubricSerializer, UserSerlializer
from .forms import UploadFileForm
from .aiscripts import ResumeScorer, ResumeParser, RubricGenerator
from PyPDF2 import PdfReader
import tempfile
import shutil

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

@api_view(['PUT'])
def update_user(request, id):
    try:
        user = User.objects.get(id=id)
        serializer = UserSerlializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(['GET'])
def getJobById(request,job_id):
    try:
        job = Job.objects.get(id=job_id)
        serializer = JobSerializer(job)
        return Response(serializer.data)
    except Job.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
 




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

@api_view(['POST'])
def post_job_by_user_id(request):
    try:
        user = User.objects.get(id=request.data['user_id'])
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = JobSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def update_job(request, job_id):
    try:
        job = Job.objects.get(id=job_id)
        serializer = JobSerializer(job, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        return Response({"message": "Job not found"}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['DELETE'])
def delete_job(request, job_id):
    try:
        job = Job.objects.get(id=job_id)
    except Job.DoesNotExist:
        return Response({'message': 'Job not found'}, status=status.HTTP_404_NOT_FOUND)

    job.delete()
    return Response({'message': 'Job was successfully deleted'}, status=status.HTTP_200_OK)

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
def add_candidate_with_generated_rubric(request, job_id):
    attributes = ["Name", "Email", "Score", "Score Description"]
    job = Job.objects.get(id=job_id)
    print(job)
    form = UploadFileForm(request.POST, request.FILES)
    if form.is_valid():

        file = request.FILES['file']
        pdf_text = []

        try:
            # Read PDF directly from the uploaded file stream
            reader = PdfReader(file)
            pdf_text = [page.extract_text() for page in reader.pages]
        except Exception as e:
            return JsonResponse({'error': f'Failed to read PDF: {str(e)}'}, status=400)

        print(request.FILES['file'])
        rubricGenerator = RubricGenerator()
        job_rubric = rubricGenerator.generate_rubric(job.jod_description)

        # Parse the resume and get the candidate data
        resumeScorer = ResumeScorer()
        candidate_score = resumeScorer.score_resume(''.join(pdf_text), job.jod_description, job_rubric)

        resumeParser = ResumeParser()
        candidate_data = resumeParser.parse_resume(candidate_score, attributes)

        # You may still want to save the candidate or log the score here
        # Depending on your application's requirements
        candidate = Candidate(
        name=candidate_data.get('Name', 'Name Not Provided'),
        resume=request.FILES['file'],
        resume_score=candidate_data.get('Score', '0'),
        resume_score_description=candidate_data.get('Score Description', 'N/A'),
        contact=candidate_data.get('Email', 'Email Not Provided'),
        job=job
    )
        candidate.save()

        # Return the score in a JSON response
        return JsonResponse(candidate_data)
    else:
        # Return an error message or invalid form notification as JSON
        return JsonResponse({'error': 'Invalid form data'}, status=400)
    
@api_view(['POST'])
def add_candidate(request, job_id):
    attributes = ["Name", "Email", "Score", "Score Description"]
    job = Job.objects.get(id=job_id)
    form = UploadFileForm(request.POST, request.FILES)
    if form.is_valid():

        file = request.FILES['file']
        pdf_text = []

        try:
            # Read PDF directly from the uploaded file stream
            reader = PdfReader(file)
            pdf_text = [page.extract_text() for page in reader.pages]
        except Exception as e:
            return JsonResponse({'error': f'Failed to read PDF: {str(e)}'}, status=400)

        # Parse the resume and get the candidate data
        resumeScorer = ResumeScorer()
        candidate_score = resumeScorer.score_resume(''.join(pdf_text), job.jod_description, job.rubric)

        resumeParser = ResumeParser()
        candidate_data = resumeParser.parse_resume(candidate_score, attributes)

        # You may still want to save the candidate or log the score here
        # Depending on your application's requirements
        candidate = Candidate(
        name=candidate_data.get('Name', 'Name Not Provided'),
        resume=request.FILES['file'],
        resume_score=candidate_data.get('Score', '0'),
        resume_score_description=candidate_data.get('Score Description', 'N/A'),
        contact=candidate_data.get('Email', 'Email Not Provided'),
        job=job
    )
        candidate.save()

        # Return the score in a JSON response
        return JsonResponse(candidate_data)
    else:
        # Return an error message or invalid form notification as JSON
        return JsonResponse({'error': 'Invalid form data'}, status=400)

@api_view(['PUT'])
def update_candidate(request, job_id):
    try:
        candidate = Candidate.objects.get(id=job_id)
        serializer = CandidateSerializer(candidate, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        return Response({"message": "Candidate not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
def delete_candidate(request, job_id):
    try:
        candidate = Candidate.objects.get(id=job_id)
    except Candidate.DoesNotExist:
        return Response({'message': 'Candidate not found'}, status=status.HTTP_404_NOT_FOUND)

    candidate.delete()
    return Response({'message': 'Candidate was successfully deleted'}, status=status.HTTP_200_OK)

@api_view(['POST'])
def post_rubric(request):
    serializer = RubricSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def get_rubric(request, id):
    try:
        rubric = Rubric.objects.get(id = id)
        serializer = RubricSerializer(rubric)
        return Response(serializer.data, status=201)
    except:
        return Response({"message": "Rubric not found"}, status=404)


@api_view(['PUT'])
def update_rubric(request, id):
    try:
        rubric = Rubric.objects.get(id=id)
        serializer = RubricSerializer(rubric, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        return Response({"message": "Rubric not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
def delete_rubric(request, id):
    try:
        rubric = Rubric.objects.get(id=id)
    except Rubric.DoesNotExist:
        return Response({'message': 'Rubric not found'}, status=status.HTTP_404_NOT_FOUND)

    rubric.delete()
    return Response({'message': 'Rubric was successfully deleted'}, status=status.HTTP_200_OK)