from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Student, Book
from .serializers import StudentSerializer, BookSerializer
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
    if request.data['age'] < 18:
        return Response({'error': 'Age must be 18 or older.'}, status=400)
    serializer = StudentSerializer(data=data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)
    # Student.objects.create(**data)
    serializer.save()
    return Response({
        'message': 'This is a placeholder for creating a record.',
        'status': 'success'
     })
    
    
@api_view(['GET'])
def get_record(request):
    if request.GET.get('id'):
        try:
            student = Student.objects.get(id=request.GET.get('id'))
            serializer = StudentSerializer(student)
            return Response({
                "data": serializer.data,
                'message': 'This is a placeholder for retrieving a single record.',
            })
        except Student.DoesNotExist:
            return Response({'error': 'Record not found.'}, status=404)
    
    obj = Student.objects.all()
    serializer = StudentSerializer(obj, many=True)
    # data = Student.objects.all().values()
    # data = list(data)
    # data = []
    # for student in Student.objects.all().order_by('-name'):
    #     data.append({
    #         'id': student.id,
    #         'name': student.name,
    #         'dob': student.dob,
    #         'email': student.email,
    #         'phone': student.phone
    #     })
    return Response({
        "data": serializer.data,
        'message': 'This is a placeholder for retrieving records.',
     })
    
    
@api_view(['DELETE'])
def delete_record(request, id):
    try:
        if id is None:
            return Response({'error': 'ID is required for deleting a record.'}, status=400)
        student = Student.objects.get(id=id)
        student.delete()
        return Response({'message': 'Record deleted successfully.'}, status=204)
    except Student.DoesNotExist:
        return Response({'error': 'Record not found.'}, status=404)
    
    
    
    
@api_view(['PUT', 'PATCH'])
def update_record(request, id):
    try:
        data = request.data
        print(data)
        # if id is None:
        if data.get('id') is None:
            return Response({'error': 'ID is required for updating a record.'}, status=400)
        student = Student.objects.get(id=id)
        serializer = StudentSerializer(student, data=data, partial=True)
        # for key, value in data.items():
        #     setattr(student, key, value)
        # student.save()
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        serializer.save()
        return Response({'message': 'Record updated successfully.'}, status=200)
    except Student.DoesNotExist:                    
        return Response({'error': 'Record not found.'}, status=404)
    
    
@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def home(request):
    if request.method == 'GET':
        if request.GET.get('id'):
            try:
                student = Student.objects.get(id=request.GET.get('id'))
                serializer = StudentSerializer(student)
                return Response({
                    "data": serializer.data,
                    'message': 'This is a placeholder for retrieving a single record.',
                })
            except Student.DoesNotExist:
                return Response({'error': 'Record not found.'}, status=404)
        data = Student.objects.all()
        serializer = StudentSerializer(data, many=True)
        return Response({
        "data": serializer.data,
        'message': 'This is a placeholder for retrieving records.',
        })
    elif request.method == 'POST':
        data = request.data
        if request.data['age'] < 18:
            return Response({'error': 'Age must be 18 or older.'}, status=400)  
        Student.objects.create(**data)
        return Response({
        'message': 'This is a placeholder for creating a record.',
        'status': 'success'
        })
    elif request.method in ['PUT', 'PATCH']:
        try:
            
            data = request.data
            if data.get('id') is None:
                return Response({'error': 'ID is required for updating a record.'}, status=400)
            student = Student.objects.get(id=request.data.get('id', id))
            serializer = StudentSerializer(student, data=data, partial=True)
            if not serializer.is_valid():
                return Response(serializer.errors, status=400)
            serializer.save()
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
    






@api_view(['POST'])
def createbook(request):
    data = request.data
    serializer = BookSerializer(data=data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)
    # Student.objects.create(**data)
    print(serializer.validated_data)
    book = serializer.save()
    print(book)
    return Response({
        'message': 'This is a placeholder for creating a record.',
        'status': 'success'
     })
    
    
@api_view(['DELETE'])
def delete_book(request, id):
    try:
        if id is None:
            return Response({'error': 'ID is required for deleting a record.'}, status=400)
        book = Book.objects.get(id=id)
        book.delete()
        return Response({'message': 'Record deleted successfully.'}, status=204)
    except Student.DoesNotExist:
        return Response({'error': 'Record not found.'}, status=404)
    
    
    
    
    
@api_view(['GET'])
def get_book(request):
    if request.GET.get('id'):
        try:
            student = Student.objects.get(id=request.GET.get('id'))
            serializer = StudentSerializer(student)
            return Response({
                "data": serializer.data,
                'message': 'This is a placeholder for retrieving a single record.',
            })
        except Student.DoesNotExist:
            return Response({'error': 'Record not found.'}, status=404)
    
    obj = Book.objects.all()
    serializer = BookSerializer(obj, many=True)
    # data = Student.objects.all().values()
    # data = list(data)
    # data = []
    # for student in Student.objects.all().order_by('-name'):
    #     data.append({
    #         'id': student.id,
    #         'name': student.name,
    #         'dob': student.dob,
    #         'email': student.email,
    #         'phone': student.phone
    #     })
    return Response({
        "data": serializer.data,
        'message': 'This is a placeholder for retrieving records.',
     })