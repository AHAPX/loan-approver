import logging

from django.http import HttpResponse, JsonResponse, Http404
from rest_framework.views import APIView
from rest_framework.response import Response

from .callcredit import search_request
from .checkers import PreChecker, CallCreditChecker
from .consts import (
    RESULT_SUCCESS, RESULT_WRONG_DATA, RESULT_REJECT_INTERNAL,
    RESULT_REJECT_CALL_CREDIT
)
from .convertors import ApplicantConvertor
from .models import Introducer, CallCredit, History
from .serializers import ApplicantSerializer


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
        serializer = ApplicantSerializer(data=data)
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
