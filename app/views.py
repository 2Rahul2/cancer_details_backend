from rest_framework import status
from rest_framework.generics import CreateAPIView
from .serializers import UserRegisterSerializer ,UserSerializer
from django.contrib.auth import authenticate ,login
from django.contrib.auth.models import User


from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

from .models import PatientDetails


class TokenVerificationView(APIView):
    permission_classes = [IsAuthenticated]  

    def get(self, request, *args, **kwargs):
        return Response({"message": "Token is valid"}, status=status.HTTP_200_OK)

class UserRegisterView(CreateAPIView):
    serializer_class = UserRegisterSerializer  # Point to your serialize
    permission_classes = [AllowAny]
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return response

class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        UserObject = User.objects.get(email=email)

        # Authenticate user
        user = authenticate(request, username=UserObject.username, password=password)
        if user is not None:
            # Successful authentication
            refresh = RefreshToken.for_user(user)
            return Response({
                'message': 'Login successful',
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),  
                'user': {
                    'username': user.username,
                    'email': user.email,
                    'id':user.id
                }
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)
        
class UserDataView(APIView):
    permission_classes = [IsAuthenticated] 

    def get(self, request , id, *args, **kwargs):
        user = request.user  
        patient_details = PatientDetails.objects.get(user=user)
        try:

            serializer = UserSerializer(patient_details)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except patient_details.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self , request ,id , *args , **kwargs):
        try:
            patient_details = PatientDetails.objects.get(user=request.user)
        except patient_details.DoesNotExist:
            return Response({"message":"user does not exist"} ,status=status.HTTP_404_NOT_FOUND)
        
        serializer = UserSerializer(patient_details , data=request.data ,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response({"message":"Error Saving Data" ,"errors": serializer.errors} ,status=status.HTTP_404_NOT_FOUND)






