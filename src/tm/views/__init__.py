import logging

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response

from tm.cache import Cache
from tm.callcredit import search_request
from tm.checkers import PreChecker, CallCreditChecker
from tm.consts import (
    RESULT_SUCCESS, RESULT_WRONG_DATA, RESULT_REJECT_INTERNAL,
    RESULT_REJECT_CALL_CREDIT
)
from tm.convertors import ApplicantConvertor
from tm.helpers import get_customer_products
from tm.models import Applicant, Introducer, CallCredit, History
from tm.serializers import SubmitSerializer
from tm.sms import send_sms


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
#            cc = CallCredit(applicant=applicant, data=data)
#            cc.extract()
#            errors = CallCreditChecker().check(cc)
#            if errors:
#                History.add(
#                    applicant,
#                    RESULT_REJECT_CALL_CREDIT,
#                    call_credit=cc,
#                    data={'fields': errors}
#                )
#                return Response({
#                    'Result': 'Rejected',
#                    'CustomerID': introducer.id,
#                    'errors': errors,
#                }, status=400)
#            History.add(applicant, RESULT_SUCCESS, call_credit=cc)
            token = Cache().get_token(applicant.id)
            redirect_url = get_customer_products(token)
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
