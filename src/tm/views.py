import logging

from django.http import HttpResponse, JsonResponse, Http404
from rest_framework.views import APIView
from rest_framework.response import Response

from .convertors import convert, SUBMIT_FIELDS
from .models import Introducer
from .serializers import ApplicantSerializer


logger = logging.getLogger(__name__)


class SubmitView(APIView):
    """
        Accept applicant data and returns response about loan decision.
    """

    def get(self, request):
        data = convert(request.query_params, SUBMIT_FIELDS)
        try:
            introducer = Introducer.objects.get(auth_code=data.get('auth_code'))
            data['introducer'] = introducer.id
        except Introducer.DoesNotFound:
            raise Http404
        serializer = ApplicantSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
