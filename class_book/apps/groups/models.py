from django.db import models
from subjects.models import Subject
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    teacher = models.BooleanField(default=False)
    group = models.BooleanField(default=True)
    student = models.BooleanField(default=False)


    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'


class Group(models.Model):
    name = models.CharField(max_length=30)
    subjects = models.ManyToManyField(Subject)

    email = models.EmailField()
    password = models.CharField(max_length=128)

    def save(self, **kwargs):
        return super().save(**kwargs)


class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
