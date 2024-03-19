from rest_framework.response import Response
from rest_framework.decorators import api_view
from core.models import *
from .serializers import UserSerlializer

@api_view(['GET'])
def getUser(request, id):
    try:
        users = User.objects.get(id = id)
        serializer = UserSerlializer(users)
        return Response(serializer.data)
    except:
        return Response({"message": "User not found"}, status=404)

@api_view(['POST'])
def addUser(request):
    serlializer = UserSerlializer(data=request.data)
    if serlializer.is_valid():
        serlializer.save()
    return Response(serlializer.data)