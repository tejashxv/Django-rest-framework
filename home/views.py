from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Student
# Create your views here.

    
    
    


@api_view(['POST','GET','PUT','PATCH','DELETE'])
def index(request):
    students = [
        {'name': 'Alice', 'age': 20, 'grade': 'A'},
        {'name': 'Bob', 'age': 22, 'grade': 'B'},
        {'name': 'Charlie', 'age': 21, 'grade': 'C'}
    ]
    data = {
        'title': 'Welcome to the Home Page',
        'message': 'This is a simple Django REST framework application.',
        'status': 'success',
        'students': students,
        "mthod": f"you are using {request.method} method",
    }
    return Response(data)


@api_view(['POST'])
def createrecord(request):
    data = request.data
    Student.objects.create(**data)
    return Response({
        'message': 'This is a placeholder for creating a record.',
        'status': 'success'
     })
    
    
@api_view(['GET'])
def get_record(request):
    # data = Student.objects.all().values()
    # data = list(data)
    data = []
    for student in Student.objects.all().order_by('-name'):
        data.append({
            'id': student.id,
            'name': student.name,
            'dob': student.dob,
            'email': student.email,
            'phone': student.phone
        })
    return Response({
        "data": data,
        'message': 'This is a placeholder for retrieving records.',
     })
    
    
@api_view(['DELETE'])
def delete_record(request, id):
    try:
        student = Student.objects.get(id=id)
        student.delete()
        return Response({'message': 'Record deleted successfully.'}, status=204)
    except Student.DoesNotExist:
        return Response({'error': 'Record not found.'}, status=404)
    
    
    
    
@api_view(['PUT', 'PATCH'])
def update_record(request, id):
    try:
        student = Student.objects.get(id=id)
        data = request.data
        for key, value in data.items():
            setattr(student, key, value)
        student.save()
        return Response({'message': 'Record updated successfully.'}, status=200)
    except Student.DoesNotExist:                    
        return Response({'error': 'Record not found.'}, status=404)
    
    
@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def home(request):
    if request.method == 'GET':
        data = []
        for student in Student.objects.all().order_by('-name'):
            data.append({
            'id': student.id,
            'name': student.name,
            'dob': student.dob,
            'email': student.email,
            'phone': student.phone
        })
        return Response({
        "data": data,
        'message': 'This is a placeholder for retrieving records.',
        })
    elif request.method == 'POST':
        data = request.data
        Student.objects.create(**data)
        return Response({
        'message': 'This is a placeholder for creating a record.',
        'status': 'success'
        })
    elif request.method in ['PUT', 'PATCH']:
        try:
            student = Student.objects.get(id=request.data.get('id', id))
            data = request.data
            for key, value in data.items():
                setattr(student, key, value)
            student.save()
            return Response({'message': 'Record updated successfully.'}, status=200)
        except Student.DoesNotExist:                    
            return Response({'error': 'Record not found.'}, status=404)
    
    elif request.method == 'DELETE':
        try:
            student = Student.objects.get(id=request.data.get('id', id))
            student.delete()
            return Response({'message': 'Record deleted successfully.'}, status=204)
        except Student.DoesNotExist:
            return Response({'error': 'Record not found.'}, status=404)
    
