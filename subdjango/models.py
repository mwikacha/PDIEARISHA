from django.db import models

class EmpProf(models.Model):
    username1=models.CharField(max_length=12,primary_key=True)
    password1=models.CharField(max_length=20)

class ManagerProf(models.Model):
    username2=models.CharField(max_length=12,primary_key=True)
    password2=models.CharField(max_length=20)

class Employee(models.Model):
    name = models.CharField(max_length=20,primary_key=True)
    address = models.CharField(max_length=100)
    telephone = models.CharField(max_length=15)
    gender = models.CharField(max_length=10)
    employment_type = models.CharField(max_length=15)
    salary = models.CharField(max_length=15)
    date = models.DateField()

class LeaveApplication(models.Model):
    startDate = models.DateField(primary_key=True)
    employeeName = models.CharField(max_length=255)
    endDate = models.DateField()
    totalDays = models.IntegerField()
    reason = models.TextField()
    medicalCertificate = models.ImageField(upload_to='medical_certificates/', blank=True, null=True)
    status = models.CharField(max_length=20, default='Pending')



