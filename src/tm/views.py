import logging

from django.http import HttpResponse, JsonResponse, Http404
from rest_framework.views import APIView
from rest_framework.response import Response

from .checkers import PreChecker
from .convertors import ApplicantConvertor
from .models import Introducer
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
            errors = PreChecker().check(serializer.instance)
            if errors:
                return Response(errors, status=400)
            # go to step2
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
