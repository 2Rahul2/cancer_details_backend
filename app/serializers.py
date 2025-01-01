from django.contrib.auth.models import User
from rest_framework import serializers
from .models import PatientDetails
import random
import string
class UserRegisterSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(write_only=True, required=True)
    name = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'phone_number', 'name']

    def create(self, validated_data):
        # Generate a random username
        random_username = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

        # Create the user
        user = User.objects.create_user(
            username=random_username,
            email=validated_data['email'],
            password=validated_data['password']
        )

        # Create the PatientDetails entry
        PatientDetails.objects.create(
            user=user,
            name=validated_data['name'],
            phone_number=validated_data['phone_number']
        )

        return user
    
class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email' ,read_only=True)
    class Meta:
        model = PatientDetails  # This can be any custom user model if you're not using the default User model
        fields = ['name', 'gender' ,'phone_number' ,'age' ,'email' ,'history']  # Specify the fields to be returned
