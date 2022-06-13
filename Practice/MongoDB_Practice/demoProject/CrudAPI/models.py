from django.db import models

# Create your models here.
class CourseDetails(models.Model):
    ID = models.AutoField(primary_key = True)
    CourseCode = models.CharField(max_length=10)
    SemesterCode = models.CharField(max_length=50)
    Section = models.IntegerField()
    Description = models.CharField(max_length=200)
