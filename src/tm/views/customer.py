import logging

from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse
from rest_framework.views import APIView
from rest_framework.response import Response

from tm.cache import Cache
from tm import consts
from tm.helpers import get_full_url
from tm.models import Applicant, Product, Template
from tm.signature import create_url_widget


logger = logging.getLogger(__name__)


class BaseCustomerStep(APIView):
    template = None

    def get_applicant(self, request):
        code = request.GET.get('code')
        try:
            return Applicant.objects.get(access_token=code)
        except Applicant.DoesNotExist:
            raise Http404

    def get_template(self):
        if self.template:
            logger.warning(self.template)
            try:
                return Template.objects.get(usefor=self.template).text
            except:
                pass
        return ''


class Step1(BaseCustomerStep):
    template = consts.LOAN_AGREEMENT

    def get(self, request):
        applicant = self.get_applicant(request)
        products = {}
        # TODO: get only suitable products
        for prod in applicant.introducer.products.all().order_by('amount', 'term'):
            if prod.amount not in products:
                products[prod.amount] = []
            products[prod.amount].append({
                'id': prod.id,
                'term': prod.term,
                'annual_rate': prod.annual_rate,
            })
        return Response({
            'step': 1,
            'template': '',
            'data': {
                'products': products,
            },
        })

    def post(self, request):
        applicant = self.get_applicant(request)
        try:
            product = Product.objects.get(id=request.data.get('product'))
        except Product.DoesNotExist:
            raise Http404
        applicant.productd = product
        applicant.save()
        return Response({
            'step': 2,
            'template': self.get_template(),
            'data': {
                'product': {
                    'amount': product.amount,
                    'term': product.term,
                    'monthly': product.annual_rate,
                    'loan_reference': 'TODO',
                },
            },
        })


class Step2(BaseCustomerStep):
    def post(self, request):
        applicant = self.get_applicant(request)
        # TODO: generate doc
        filename = '/tmp/testdoc.txt'
        open(filename, 'w').write('test test sign and go')
        token = Cache().get_token(applicant.id)
        logger.warning(get_full_url(reverse('customer_signature', kwargs={'token': token})))
        url = create_url_widget(filename, get_full_url(reverse('customer_signature', kwargs={'token': token})))
        return Response({'redirect_url': url})


class Step3(BaseCustomerStep):
    def get(self, request):
        applicant = self.get_applicant(request)
        return Response({
            'step': 3,
            'template': self.get_template(),
            'data': {},
        })


def main(request, token):
    cache = Cache()
    app_id = cache.get(token)
    try:
        applicant = Applicant.objects.get(id=app_id)
        cache.delete(token)
    except Applicant.DoesNotExist:
        raise Http404
    return redirect('{}?code={}'.format(
        reverse('customer_step1'),
        applicant.access_token)
    )


def signature(request, token):
    cache = Cache()
    app_id = cache.get(token)
    try:
        applicant = Applicant.objects.get(id=app_id)
        cache.delete(token)
    except Applicant.DoesNotExist:
        raise Http404
    return redirect('{}?code={}'.format(
        reverse('customer_step3'),
        applicant.access_token)
    )
