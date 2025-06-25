"""
URL configuration for djrest project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from home.views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'product/v2', ProductViewSet, basename='product')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', index, name='index'),
    path('api/createrecord/', createrecord, name='createrecord'),
    path('api/get_record/', get_record, name='get_record'),
    path('api/delete_record/<int:id>', delete_record, name='delete_record'),
    path('api/update_record/<int:id>', update_record, name='update_record'),
    path('api/home/', home, name='home'),
    path('api/createbook/', createbook, name='createbook'),
    path('api/delete_book/<int:id>', delete_book, name='delete_book'),
    path('api/get_book/', get_book, name='get_book'),
    path('api/create_user/', create_user, name='create_user'),
    path('api/get_newbook/', get_newbook, name='get_newbook'),
    path('api/v2/students/', StudentAPI.as_view(), name='student_api'),
    path('api/v3/student s/', StudentModelListView.as_view(), name='student_model_list'),
    path('api/v4/students/<pk>', StudentModelListView.as_view(), name='student_model_delete'),
    path('api/products/', ProductListCreate.as_view(), name='product_list_create'),
    path('api/products/<int:pk>', ProductListCreate.as_view(), name='product_list_create'),
    path('api/', include(router.urls)),
]





