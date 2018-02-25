import logging

from django.http import HttpResponse, JsonResponse, Http404
from django.contrib.auth.models import User
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from .callcredit import search_request
from .checkers import PreChecker, CallCreditChecker
from .consts import (
    RESULT_SUCCESS, RESULT_WRONG_DATA, RESULT_REJECT_INTERNAL,
    RESULT_REJECT_CALL_CREDIT
)
from .convertors import ApplicantConvertor
from .models import (
    Applicant, Introducer, CallCredit, History, Template, Setting, Product
)
from .serializers import (
    SubmitSerializer, ApplicantSerializer, IntroducerSerializer,
    TemplateSerializer, SettingSerializer, UserSerializer, ProductSerializer
)


logger = logging.getLogger(__name__)


class SubmitView(APIView):
    """
        Accept applicant data and returns response about loan decision.
    """

    def get(self, request):
        data = ApplicantConvertor().convert(request.query_params)
        try:
            introducer = Introducer.objects.get(auth_code=data.get('auth_code'))
            data['introducer'] = introducer.id
        except Introducer.DoesNotFound:
            raise Http404
        serializer = SubmitSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            a1 = serializer.instance
            applicant = serializer.instance
            errors = PreChecker().check(applicant)
            if errors:
                History.add(
                    applicant,
                    RESULT_REJECT_INTERNAL,
                    data={'fields': errors}
                )
                return Response({
                    'Result': 'Invalid Data',
                    'CustomerID': introducer.id,
                    'Error': 'Invalid Format',
                }, status=400)
            try:
                data = search_request(applicant)
            except Exception as e:
                logger.error(e)
                History.add(applicant, RESULT_WRONG_DATA)
                return Response({
                    'Result': 'Invalid Data',
                    'CustomerID': introducer.id,
                    'Error': 'Invalid Format',
                }, status=400)
            cc = CallCredit(applicant=applicant, data=data)
            cc.extract()
            errors = CallCreditChecker().check(cc)
            if errors:
                History.add(
                    applicant,
                    RESULT_REJECT_CALL_CREDIT,
                    call_credit=cc,
                    data={'fields': errors}
                )
                return Response({
                    'Result': 'Rejected',
                    'CustomerID': introducer.id,
                }, status=400)
            History.add(applicant, RESULT_SUCCESS, call_credit=cc)
            return Response({
                'Result': 'Accepted',
                'CustomerID': introducer.id,
                'RedirectURL': '#TODO',
                'Commission': '#TODO',
                'Amount': '#TODO',
            })
        return Response({
            'Result': 'Invalid Data',
            'CustomerID': introducer.id,
            'Error': 'Mandatory Field',
        }, status=400)


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
