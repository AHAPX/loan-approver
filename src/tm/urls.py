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
from rest_framework.documentation import include_docs_urls

from tm.views import SubmitView, admin as admin_v, customer


urlpatterns = [
    path('v1/', include('rest_framework.urls')),
    path('v1/applicants/', admin_v.ApplicantList.as_view()),
    path('v1/applicants/<int:pk>/', admin_v.ApplicantDetail.as_view()),
    path('v1/introducers/', admin_v.IntroducerList.as_view()),
    path('v1/introducers/<int:pk>/', admin_v.IntroducerDetail.as_view()),
    path('v1/products/', admin_v.ProductList.as_view()),
    path('v1/products/<int:pk>/', admin_v.ProductDetail.as_view()),
    path('v1/templates/', admin_v.TemplateList.as_view()),
    path('v1/templates/<int:pk>/', admin_v.TemplateDetail.as_view()),
    path('v1/users/', admin_v.UserList.as_view()),
    path('v1/users/<int:pk>/', admin_v.UserDetail.as_view()),
    path('v1/settings/', admin_v.SettingView.as_view(), name='setting'),
# customer steps
    path('a/<token>', customer.main, name='customer_main'),
    path('sign/<token>', customer.signature, name='customer_signature'),
    path('v1/customer/step1/', customer.Step1.as_view(), name='customer_step1'),
    path('v1/customer/step2/', customer.Step2.as_view(), name='customer_step2'),
    path('v1/customer/step3/', customer.Step3.as_view(), name='customer_step3'),
# main
    path('submit/', SubmitView.as_view(), name='submit'),
    path('admin/', admin.site.urls),
    path('docs/', include_docs_urls(title='TMA API')),
]
