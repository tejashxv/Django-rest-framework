from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializers import StudentSerializer, BookSerializer, UserSerializer,CreateBookSerializer,NewBookSerializer, ProductSerializer, RegisterSerializer , LoginSerializer
from rest_framework.views import APIView 
from rest_framework.mixins import ListModelMixin, CreateModelMixin, DestroyModelMixin
from rest_framework.generics import GenericAPIView, ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.decorators import action
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication

class RegisterAPI(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'User registered successfully.',
                'status': 'success',
                'data': serializer.data
            })
        return Response({
            'error': serializer.errors,
            'status': 'error'
            
        }, status=400)
        
    def get(self, request):
        users = User.objects.all()
        serializer = RegisterSerializer(users, many=True)
        return Response({
            'message': 'This is a placeholder for retrieving all users.',
            'status': 'success',
            'data': serializer.data
        })
        
    

class LoginAPI(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password']
            )
            
            if not user:
                return Response({
                    'error': 'Invalid credentials.',
                    'status': 'error'
                }, status=400)
            
            token,create = Token.objects.get_or_create(user=user)
            
            
            
            return Response({
                'message': 'User registered successfully.',
                'status': 'success',
                'data': serializer.data,
                "token": token.key
            })
        return Response({
            'error': serializer.errors,
            'status': 'error'
            
        }, status=400)


# class LogoutAPI(APIView):
    


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    
    @action(detail=False, methods=['POST'])
    def export_product(self, request):
        return Response({
            "status": "success",
            "message": "This is a placeholder for exporting records.",
            "data": self.get_queryset().values('name', 'price', 'description')
        })
        
    @action(detail=True, methods=['POST'])
    def email_sent(self, request, pk):
        print("email sent", pk)
        return Response({
            "status": "success",
            "message": "This is a placeholder for sending email.",
            "data": {}
        })
    
    
# Create your views here. 

class ProductListCreate(generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    
    
    def list(self, request, *args, **kwargs):
        print(request.user)
        return super().list(request, *args, **kwargs)
    # def list(self, request, *args, **kwargs):
    #     response = super().list(request, *args, **kwargs)
    #     response.data = {
    #         "status": "success",
    #         "message": "This is a placeholder for retrieving records.",
    #         "data": response.data
    #     }
    #     return response
    
    # def preform_create(self, serializer):
    #     serializer.save(created_by=self.request.user)
    #     return super().perform_create(serializer)

class StudentModelListView(ListModelMixin, GenericAPIView,CreateModelMixin,DestroyModelMixin):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    # def get_queryset(self):
    #     return Student.objects.filter(name__startswith='r')
    
    def perform_create(self, serializer):
        print("perform_create")
        return super().perform_create(serializer)
    
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly

class StudentAPI(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    # authentication_classes = [TokenAuthentication]
    
    def get(self, request):
        try:
            student = Student.objects.all().order_by('-name')
            serializer = StudentSerializer(student, many=True)
            return Response({
                "data": serializer.data,
                'message': 'This is a placeholder for retrieving a single record.',
            })
        except Student.DoesNotExist:
            return Response({'error': 'Record not found.'}, status=404)
        
    def post(self, request):
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
        
    def delete(self,request):
        try:
            id = request.data.get('id')
            if id is None:
                return Response({'error': 'ID is required for deleting a record.'}, status=400)
            student = Student.objects.get(id=id)
            student.delete()
            return Response({'message': 'Record deleted successfully.'}, status=204)
        except Student.DoesNotExist:
            return Response({'error': 'Record not found.'}, status=404)


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
    serializer = NewBookSerializer(data=data)
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
            student = Book.objects.get(id=request.GET.get('id'))
            serializer = NewBookSerializer(student)
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
    
    
    
    
    
    

@api_view(['POST'])
def create_user(request):
    data = request.data
    
    serializer = UserSerializer(data=data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)
    # Student.objects.create(**data)
    print(serializer.validated_data)
    user = serializer.save()
    print(user)
    return Response({
        'message': 'This is a placeholder for creating a record.',
        'status': 'success'
     })
    
    
@api_view(['GET'])
def get_newbook(request):
    data = Book.objects.all()
    serializer = NewBookSerializer(data, many=True)
    return Response({
        'message': 'This is a placeholder for creating a record.',
        'status': 'success',
        'data' : serializer.data
     })
    
    
