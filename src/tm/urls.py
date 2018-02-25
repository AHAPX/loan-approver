"""tm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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

from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1/', include('rest_framework.urls')),
    path('v1/applicants/', views.ApplicantList.as_view()),
    path('v1/applicants/<int:pk>/', views.ApplicantDetail.as_view()),
    path('v1/introducers/', views.IntroducerList.as_view()),
    path('v1/introducers/<int:pk>/', views.IntroducerDetail.as_view()),
    path('v1/products/', views.ProductList.as_view()),
    path('v1/products/<int:pk>/', views.ProductDetail.as_view()),
    path('v1/templates/', views.TemplateList.as_view()),
    path('v1/templates/<int:pk>/', views.TemplateDetail.as_view()),
    path('v1/users/', views.UserList.as_view()),
    path('v1/users/<int:pk>/', views.UserDetail.as_view()),
    path('v1/settings/', views.SettingView.as_view(), name='setting'),
    path('submit/', views.SubmitView.as_view(), name='submit'),
]
