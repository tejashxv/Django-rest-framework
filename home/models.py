from django.db import models
import uuid
from django.contrib.auth.models import User
# Create your models here.


class UserExtended(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='extended_profile')
    is_vip = models.BooleanField(default=False)
 
    def __str__(self):
        return f"{self.user.username} - VIP: {self.is_vip}"

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
    

def generateSlug():
    return str(uuid.uuid4())

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.FloatField()
    product_slug = models.SlugField(default=generateSlug)
    in_stock = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products', null=True, blank=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['in_stock'], name='product_in_stock_idx', condition=models.Q(in_stock=True))
        ]