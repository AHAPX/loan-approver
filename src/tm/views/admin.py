from django.contrib.auth.models import User
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from tm.models import Applicant, Introducer, Template, Setting, Product
from tm.serializers import (
    ApplicantSerializer, IntroducerSerializer, TemplateSerializer,
    SettingSerializer, UserSerializer, ProductSerializer
)


class ApplicantList(generics.ListAPIView):
    queryset = Applicant.objects.all()
    serializer_class = ApplicantSerializer
    permission_classes = (permissions.IsAdminUser,)


class ApplicantDetail(generics.RetrieveUpdateAPIView):
    queryset = Applicant.objects.all()
    serializer_class = ApplicantSerializer
    permission_classes = (permissions.IsAdminUser,)


class IntroducerList(generics.ListCreateAPIView):
    queryset = Introducer.objects.all()
    serializer_class = IntroducerSerializer
    permission_classes = (permissions.IsAdminUser,)


class IntroducerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Introducer.objects.all()
    serializer_class = IntroducerSerializer
    permission_classes = (permissions.IsAdminUser,)


class TemplateList(generics.ListCreateAPIView):
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer
    permission_classes = (permissions.IsAdminUser,)


class TemplateDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer
    permission_classes = (permissions.IsAdminUser,)


class SettingView(APIView):
    permission_classes = (permissions.IsAdminUser,)
    fields = (
        'age_max', 'age_min', 'employment_status', 'income_min',
        'loan_amount_min', 'loan_amount_max', 'employer', 'occupation',
        'postcode',
    )

    def get(self, request):
        setting = Setting.get_setting()
        data = {}
        for field in self.fields:
            data[field] = getattr(setting, field, None)
        return Response(data)

    def put(self, request):
        setting = Setting.get_setting()
        serializer = SettingSerializer(instance=setting, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdminUser,)


class UserDetail(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdminUser,)


class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (permissions.IsAdminUser,)


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (permissions.IsAdminUser,)


