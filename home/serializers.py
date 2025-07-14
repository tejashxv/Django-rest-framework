from rest_framework import serializers
from .models import *
from datetime import date
import uuid
from .validators import *
from django.contrib.auth.models import User

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, validators=[no_numbers])
    password = serializers.CharField(max_length=128)
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=150)
    
    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("Username already exists.")
        return username
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        return user
    
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, validators=[no_numbers])
    password = serializers.CharField(max_length=128)
    
    # def validate(self, attrs):
    #     if not User.objects.filter(username=attrs['username']).exist():
    #         return serializers.ValidationError("User does not exist.")
    #     user = User.objects.get(username=attrs['username'])
    #     if not user.check_password(attrs['password']):
    #         return serializers.ValidationError("Incorrect password.")
    
    
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student 
        # fields = ['id', 'name', 'dob', 'email', 'phone']
        fields = '__all__'
        # exclude = ['id']  
    
    def calculate_age(self, dob):
        today = date.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        # print(f"Calculated age: {age}")
        return age
    
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['age'] = self.calculate_age(instance.dob)
        return data
    
    def create(self, validated_data):
        student = Student.objects.create(**validated_data)
        student.student_id = str(uuid.uuid4())  # Generate a unique student ID
        student.save()
        return student

    def update(self, instance, validated_data):
        student_id = str(uuid.uuid4())
        name = validated_data.get('name', instance.name)
        dob = validated_data.get('dob', instance.dob)
        email = validated_data.get('email', instance.email)
        phone = validated_data.get('phone', instance.phone)
        # age = validated_data.get('age', instance.age)  # This line is not needed as age is calculated in to_representation
        if student_id is None:
            instance.student_id = student_id
        instance.name = name
        instance.dob = dob
        instance.email = email
        instance.phone = phone
        # instance.age = age  # This line is not needed as age is calculated in to_representation
        instance.save()
        return instance
    
    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        if 'name' in data:
            data['name'] = data['name'].strip()  # Remove leading/trailing spaces from name
        
        return super().to_internal_value(data)
    
    def get_fields(self):
        fields =  super().get_fields()
        print("Fields in StudentSerializer:", fields)
        return fields
        
from rest_framework.validators import UniqueValidator
class BookSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)  
    title = serializers.CharField(max_length=200,
                                  validators=[UniqueValidator(
                                      queryset=Book.objects.all())
                                    ])  
    author = serializers.CharField(max_length=100)
    price = serializers.FloatField()
    
    
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'title': instance.title,
            'author': instance.author,
            'price': round(instance.price * 1.08, 2)  # 8% GST added and rounded to 2 decimals
        }
    
    
    def create(self, validated_data):
        return Book.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        title = validated_data.get('title', instance.title)
        author = validated_data.get('author', instance.author)
        price = validated_data.get('price', instance.price)
        instance.title = title
        instance.author = author
        instance.price = price
        instance.save()
        return instance
    
    
class AddressSerializer(serializers.Serializer):
    city = serializers.CharField(max_length=50)
    zip_code = serializers.CharField(max_length=10)
    
    def validate_zip_code(self, value):
        if not value.isdigit() or len(value) != 5:
            raise serializers.ValidationError("Zip code must be a 5-digit number.")
        return value
    
    def create(self, validated_data):
        return {
            'city': validated_data['city'],
            'zip_code': validated_data['zip_code']
        }
    
    
     
class UserSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100,
                                validators=[no_numbers],
                                error_messages={
                                    'max_length': 'Name must be at most 100 characters long.',
                                    'required': 'Name is required.'
                                })
    email = serializers.EmailField(validators=[email_validator],
                                  error_messages={
                                      'invalid': 'Email must be a valid email address.',
                                      'required': 'Email is required.'
                                  })
    age = serializers.IntegerField()
    phone = serializers.RegexField(
        regex=r'^\+?1?\d{9,15}$',
        error_messages={
            'invalid': 'Phone number must be entered in the format: "+999999999". Up to 15 digits allowed.'
        }
    )
    address = AddressSerializer()
    user_type = serializers.ChoiceField(
        choices=['admin', 'user', 'guest'])
    admin_code  = serializers.CharField(required=False)
        
     
    def validate(self, attrs):
        if attrs.get('age') < 18:
            raise serializers.ValidationError("Age must be at least 18 years old.")
        if not attrs.get('email').endswith('@gmail.com'):
            raise serializers.ValidationError("Email domain must be 'example.com'.")
        if attrs.get('user_type') == 'admin' and not attrs.get('admin_code'):
            return serializers.ValidationError("Admin code is required for admin users.")
        return attrs    
    
    # def validate_age(self, attrs):
    #     if attrs.get('age') < 18:
    #         raise serializers.ValidationError("Age must be at least 18 years old.")
    #     return super().validate(attrs)
    
    
    # def validate_email(self, value):
    #     if value.split('@')[1] != 'gmail.com':
    #         raise serializers.ValidationError("Email domain must be 'example.com'.")
    #     return value
    def create(self, validated_data):
        return {
            'name': validated_data['name'],
            'email': validated_data['email'],
            'age': validated_data['age'],
            'phone': validated_data['phone']
        }
        
        
        
        


class PublisherSerializer(serializers.ModelSerializer):
     class Meta:
         model = Publisher
         fields = '__all__'

class AuthorSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Author 
        fields = '__all__'
        
        
class CreateBookSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset = Author.objects.all())
    publisher = serializers.PrimaryKeyRelatedField(queryset = Publisher.objects.all(), many = True)
    class Meta:
        model = Book
        fields = '__all__'
        
        
class NewBookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    publisher = PublisherSerializer(many=True)
    
    class Meta:
        model = Book
        fields = '__all__'
    
    def create(self, validated_data):
        author = validated_data.pop('author')
        publisher_data = validated_data.pop('publisher')
        author,_ = Author.objects.get_or_create(**author)
        book = Book.objects.create(author=author, **validated_data)
        for publisher in publisher_data:
            publisher_obj,_ = Publisher.objects.get_or_create(**publisher)
            book.publisher.add(publisher_obj)
        return book