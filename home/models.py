from django.db import models

# Create your models here.


class Student(models.Model):
    student_id = models.CharField(null=True, blank=True)
    name = models.CharField(max_length=100)
    dob = models.DateField()
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    
    
    
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    price = models.FloatField()
    
    
    def __str__(self):
        return self.title
    
