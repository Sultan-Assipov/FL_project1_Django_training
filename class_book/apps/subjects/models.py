from django.db import models


class Subject(models.Model):
    name = models.CharField(max_length=30)
    level_3 = models.FloatField(default=25)
    level_4 = models.FloatField(default=50)
    level_5 = models.FloatField(default=75)
    attendance_score = models.FloatField(default=0)


class Task(models.Model):
    name = models.CharField(max_length=30)
    deadline = models.DateField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    max_score = models.PositiveIntegerField()


class Lesson(models.Model):
    name = models.CharField(max_length=30)
    date = models.DateField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
