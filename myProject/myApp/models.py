from django.db import models

# Create your models here.
class Registerdb(models.Model):
    name=models.CharField(max_length=30)
    email=models.EmailField()
    password=models.CharField(max_length=20)
    cpassword=models.CharField(max_length=20)
    status=models.BooleanField(default=False)
