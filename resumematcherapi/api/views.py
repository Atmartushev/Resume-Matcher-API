from rest_framework.response import Response
from rest_framework.decorators import api_view
from core.models import *
from .serializers import UserSerlializer

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
    serlializer = UserSerlializer(data=request.data)
    if serlializer.is_valid():
        serlializer.save()
    else:
        return Response({"message": "Invalid user data"}, status=404)
    return Response(serlializer.data)