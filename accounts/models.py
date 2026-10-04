from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class StudentProfile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    name = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    usn = models.CharField(
        max_length=20,
        unique=True
    )

    branch = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    semester = models.PositiveIntegerField(
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.name} - {self.usn}"