from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.auth import AuthToken
from .serializers import RegisterSerializer, UpdateUserSerializer

def serialize_user(user):
    return {
        "username": user.username,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name
    }



@api_view(['POST'])
def login(request):
    serializer = AuthTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']
    _, token = AuthToken.objects.create(user)
    return Response({
        'user_data': serialize_user(user),
        'token': token
    })
        

@api_view(['POST'])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        user = serializer.save()
        _, token = AuthToken.objects.create(user)
        return Response({
            "user_info": serialize_user(user),
            "token": token
        })

@api_view(['POST'])
def update(request):
    user = request.user
    if user.is_authenticated:
        serializer = UpdateUserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):

            new_user = serializer.update(user, request.data)
            if(new_user == 0):
                return Response({'error': 'Name is not None'}, status=400)
            if(new_user == 1):
                return Response({'error': 'Email is already in use'}, status=400)

        return Response({
            'user_info': serialize_user(new_user),
        })
    return Response({'error': 'not authenticated'}, status=400)


@api_view(['GET'])
def get_user(request):
    username = request.user
    if username.is_authenticated:
        return Response({
            'user_data': serialize_user(username)
        })
    return Response({'error': 'not authenticated'}, status=400)