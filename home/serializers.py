from rest_framework import serializers
from .models import Student, Book
from datetime import date
import uuid

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
        
        
class BookSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)  
    title = serializers.CharField(max_length=200)
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
    
    
    
    
    
class UserSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    age = serializers.IntegerField()
    phone = serializers.RegexField(
        regex=r'^\+?1?\d{9,15}$',
        error_messages={
            'invalid': 'Phone number must be entered in the format: "+999999999". Up to 15 digits allowed.'
        }
    )
    
    def validate(self, attrs):
        if attrs.get('age') < 18:
            raise serializers.ValidationError("Age must be at least 18 years old.")
        if not attrs.get('email').endswith('@example.com'):
            raise serializers.ValidationError("Email domain must be 'example.com'.")
        return attrs    
    
    # def validate_age(self, attrs):
    #     if attrs.get('age') < 18:
    #         raise serializers.ValidationError("Age must be at least 18 years old.")
    #     return super().validate(attrs)
    
    
    # def validate_email(self, value):
    #     if value.split('@')[1] != 'gmail.com':
    #         raise serializers.ValidationError("Email domain must be 'example.com'.")
    #     return value