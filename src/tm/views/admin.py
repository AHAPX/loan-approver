import logging
from io import BytesIO

from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.http import Http404, HttpResponse
from django.template import Template, Context
from drf_pdf.renderer import PDFRenderer
from drf_pdf.response import PDFResponse
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from xhtml2pdf import pisa

from tm.models import Applicant, Introducer, Template as TemplateM, Setting, Product
from tm.serializers import (
    ApplicantSerializer, IntroducerSerializer, TemplateSerializer,
    SettingSerializer, UserSerializer, ProductSerializer
)


logger = logging.getLogger(__name__)


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
    queryset = TemplateM.objects.all()
    serializer_class = TemplateSerializer
    permission_classes = (permissions.IsAdminUser,)


class TemplateDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TemplateM.objects.all()
    serializer_class = TemplateSerializer
    permission_classes = (permissions.IsAdminUser,)


class TemplateBaseRender(APIView):
    permission_classes = (permissions.IsAdminUser,)

    def render(self, lrn, template_id):
        if not lrn:
            raise Http404
        try:
            applicant = Applicant.objects.get(access_token=lrn)
        except Applicant.DoesNotExist:
            raise Http404
        try:
            template = TemplateM.objects.get(id=template_id)
        except:
            raise Http404
        return Template(template.text).render(Context({
            'applicant': applicant,
            'product': applicant.product,
            'introducer': applicant.introducer,
        })), template


class TemplatePreview(TemplateBaseRender):
    renderer_classes = (PDFRenderer,)

    def get(self, request, pk):
        lrn = request.GET.get('loanrefnumber')
        text, template = self.render(lrn, pk)
        kind = request.GET.get('kind')
        if kind == 'pdf':
            pdf = BytesIO()
            pisa.CreatePDF(text, pdf)
            rendered = pdf.getvalue()
            pdf.close()
            return PDFResponse(rendered, file_name=f'{template.name}-{lrn}.pdf')
        else:
            return HttpResponse(content=text.encode('utf-8'))


class TemplateSendEmail(TemplateBaseRender):
    def post(self, request, pk):
        lrn = request.GET.get('loanrefnumber')
        text, template = self.render(lrn, pk)
        to_email = request.POST.get('to')
        logger.warning(to_email)
        message = EmailMessage(
            subject=f'Render of {template.name} for lrn {lrn}.',
            body=text,
            to=[to_email]
        )
        if message.send() == 0:
            return Response({'message': 'No messages has been sent.'}, status=500)
        return Response(status=200)


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
