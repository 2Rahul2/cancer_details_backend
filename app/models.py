from django.db import models

from django.contrib.auth.models import User

# Create your models here.
class PatientDetails(models.Model):
    class GenderChoices(models.TextChoices):
        MALE = "Male" ,"Male"
        FEMALE = 'Female', 'Female'
        OTHER = 'Other', 'Other'
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    age = models.PositiveSmallIntegerField(null=True)
    gender = models.CharField(max_length=10 ,choices=GenderChoices.choices ,null=True)
    phone_number = models.PositiveIntegerField(max_length=10 ,null=True)

