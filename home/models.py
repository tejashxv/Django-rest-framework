from django.db import models

# Create your models here.


class Student(models.Model):
    student_id = models.CharField(null=True, blank=True)
    name = models.CharField(max_length=100)
    dob = models.DateField()
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    
   
class Author(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Publisher(models.Model):
    name = models.CharField(max_length=100)   
    website = models.URLField()
    
    def __str__(self):
        return self.name
    
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='book_publisher', null=True, blank=True)
    publisher = models.ManyToManyField(Publisher, related_name='books')
    
    
    def __str__(self):
        return self.title
    
