import logging

from django.contrib.auth import authenticate
from django.db.models import Q
from django.http import Http404
from django.urls import reverse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from tm.cache import Cache
from tm.callcredit import search_request
from tm.checkers import PreChecker, CallCreditChecker
from tm.consts import (
    RESULT_SUCCESS, RESULT_WRONG_DATA, RESULT_REJECT_INTERNAL,
    RESULT_REJECT_CALL_CREDIT
)
from tm.convertors import ApplicantConvertor
from tm.helpers import get_full_url
from tm.models import Applicant, Introducer, CallCredit, History
from tm.serializers import (
    SubmitSerializer, RegisterSerializer, VerifySerializer, ApplicantSerializer,
    LoginSerializer
)
from tm.sms import send_sms


logger = logging.getLogger(__name__)


class LoginView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            return Response({'user': request.user.username})
        return Response(status=401)

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                username=serializer.data['username'],
                password=serializer.data['password']
            )
            if user is not None:
                return Response(data={'message': 'login successful'})
        return Response(serializer.errors, status=400)


class RegisterView(APIView):
    def get(self, request):
        serializer = RegisterSerializer(data=request.query_params)
        if serializer.is_valid():
            introducer = Introducer.objects.create(ip=serializer.data['ip'])
            return Response({'auth': introducer.auth_code})
        return Response(serializer.errors, status=400)


class VerifyView(APIView):
    def get(self, request):
        serializer = VerifySerializer(data=request.query_params)
        if serializer.is_valid():
            try:
                introducer = Introducer.objects.get(auth_code=serializer.data['auth'])
                return Response(status=200)
            except Introducer.DoesNotExist:
                raise Http404
        return Response(serializer.errors, status=400)


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
# call credir checking
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
                    'errors': errors,
                }, status=400)
            History.add(applicant, RESULT_SUCCESS, call_credit=cc)
# checking success, send sms
            token = Cache().get_token(applicant.id)
            redirect_url = get_full_url(reverse('customer_main', kwargs={'token': token}))
#            send_sms(applicant.phone_mobile, redirect_url)
            return Response({
                'Result': 'Accepted',
                'CustomerID': introducer.id,
                'RedirectURL': redirect_url,
                'Commission': '#TODO',
                'Amount': '#TODO',
            })
        return Response({
            'Result': 'Invalid Data',
            'CustomerID': introducer.id,
            'Error': 'Mandatory Field',
        }, status=400)


class ApplicantSearchView(APIView):
    permission_classes = (permissions.IsAdminUser,)
    fields = {
        'loanrefnumber': 'access_token',
        'first_name': 'first_name',
        'last_name': 'last_name',
        'phone_landline': 'phone_laldline',
        'phone_mobile': 'phone_mobile',
        'postcode': 'addr_postcode',
    }

    def get(self, request):
        query = Q()
        for param, field in self.fields.items():
            if param in request.query_params:
                query &= Q(**{field: request.query_params[param]})
        applicants = Applicant.objects.filter(query)
        data = [ApplicantSerializer(instance=app).data for app in applicants]
        return Response({'applicants': data})
