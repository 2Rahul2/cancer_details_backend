from rest_framework import status
from rest_framework.generics import CreateAPIView
from .serializers import UserRegisterSerializer ,UserSerializer
from django.contrib.auth import authenticate ,login


from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken


class TokenVerificationView(APIView):
    permission_classes = [IsAuthenticated]  

    def get(self, request, *args, **kwargs):
        return Response({"message": "Token is valid"}, status=status.HTTP_200_OK)

class UserRegisterView(CreateAPIView):
    serializer_class = UserRegisterSerializer  # Point to your serializer
    permission_classes = [AllowAny]
    def create(self, request, *args, **kwargs):
        # Optionally, add custom logic here, such as sending a welcome email
        response = super().create(request, *args, **kwargs)
        return response

class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        # Authenticate user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Successful authentication
            refresh = RefreshToken.for_user(user)

            return Response({
                'message': 'Login successful',
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),  # Optionally, you can return the refresh token
                'user': {
                    'username': user.username,
                    'email': user.email,
                    'id':user.id
                }
            }, status=status.HTTP_200_OK)
        else:
            # Authentication failed
            return Response({'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)
        
class UserDataView(APIView):
    permission_classes = [IsAuthenticated]  # Optional, ensure the user is authenticated

    def get(self, request , id, *args, **kwargs):
        print(id)
        # Assuming the user is authenticated, return the user's data
        user = request.user  # Get the current authenticated user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)





