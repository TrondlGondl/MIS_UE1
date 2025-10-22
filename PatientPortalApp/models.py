from django.db import models
from django.contrib.auth.models import User

class Practitioner(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)


class Patient(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    practitioner = models.ForeignKey(Practitioner, null=True, on_delete=models.SET_NULL)

    questionare_completed = models.BooleanField(default=False)
    questionare_data = models.JSONField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    activated_at = models.DateField(null=True)

    SVNR = models.CharField(max_length=11)
    birthday = models.DateTimeField()




class Questionaire_Template(models.Model):
    questions = models.JSONField()
    version = models.IntegerField()
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


