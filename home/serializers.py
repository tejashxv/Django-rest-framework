from rest_framework import serializers
from .models import Student, Book


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student 
        # fields = ['id', 'name', 'dob', 'email', 'phone']
        fields = '__all__'
        # exclude = ['id']  
        
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