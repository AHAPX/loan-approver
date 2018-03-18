import logging

from django.db import transaction
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse
from rest_framework.views import APIView
from rest_framework.response import Response

from tm.cache import Cache
from tm import consts
from tm.helpers import get_full_url
from tm.models import Applicant, Product, Template, LoanOutstand
from tm.serializers import (
    CustomerStep3, CustomerStep4, CustomerStep5, CustomerStep6, CustomerStep7,
    CustomerStep8
)
from tm.signature import create_url_widget
from tm.sms import send_sms


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

    def response(self, step, data={}):
        return Response({
            'step': step,
            'template': self.get_template(),
            'data': data,
        })

    def error(self, errors):
        return Response({'errors': errors})


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
        return self.response(1, {'products': products})

    def post(self, request):
        applicant = self.get_applicant(request)
        try:
            product = Product.objects.get(id=request.data.get('product'))
        except Product.DoesNotExist:
            raise Http404
        applicant.product = product
        applicant.save()
        return self.response(2, {'product': {
            'amount': product.amount,
            'term': product.term,
            'monthly': product.annual_rate,
            'loan_reference': 'TODO',
        }})


class Step2(BaseCustomerStep):
    def get(self, request):
        applicant = self.get_applicant(request)
        if not applicant.product:
            return self.error(['product not choosen'])
        return self.response(2, {'product': {
            'amount': applicant.product.amount,
            'term': applicant.product.term,
            'monthly': applicant.product.annual_rate,
            'loan_reference': 'TODO',
        }})

    def post(self, request):
        applicant = self.get_applicant(request)
        # TODO: generate doc
        filename = '/tmp/testdoc.txt'
        open(filename, 'w').write('test test sign and go')
        token = Cache().get_token(applicant.id)
        url = create_url_widget(filename, get_full_url(reverse('customer_signature', kwargs={'token': token})))
        return self.response(2, {'redirect_url': url})


class Step3(BaseCustomerStep):

    def get_data(self, applicant):
        return {'product': {
            'amount': applicant.product.amount,
            'term': applicant.product.term,
            'monthly': applicant.product.annual_rate,
            'loan_reference': 'TODO',
            'account_number': applicant.bank_account_number,
            'sort_code': applicant.bank_sort_code,
            'pay_frequency': applicant.bank_pay_frequency,
        }}

    def get(self, request):
        applicant = self.get_applicant(request)
        if not applicant.product:
            return self.error(['product not choosen'])
        return self.response(3, self.get_data(applicant))

    def post(self, request):
        applicant = self.get_applicant(request)
        serializer = CustomerStep3(data=request.data)
        if serializer.is_valid():
            applicant.bank_account_number = serializer.data['account_number']
            applicant.bank_sort_code = serializer.data['sort_code']
            applicant.bank_pay_frequency =  serializer.data['pay_frequency']
            applicant.save()
            return self.response(4, self.get_data(applicant))
        return self.error(serializer.errors)


class Step4(BaseCustomerStep):
    def get_data(self, applicant):
        return {
            'rent_mortgage': applicant.rent_mortgage,
            'live_with': applicant.live_with,
            'children': applicant.children,
            'child_care_costs': applicant.child_care_costs,
            'cars': applicant.cars,
            'loan_purpose': applicant.loan_purpose,
            'loans': [{
                'lender': l.lender,
                'amount': l.amount,
            } for l in applicant.loans.all()]
        }

    def get(self, request):
        applicant = self.get_applicant(request)
        return self.response(4, self.get_data(applicant))

    def post(self, request):
        applicant = self.get_applicant(request)
        serializer = CustomerStep4(data=request.data)
        if serializer.is_valid():
            with transaction.atomic():
                applicant.rent_mortgage = serializer.data['rent_mortgage']
                applicant.live_with = serializer.data['live_with']
                applicant.children =  serializer.data['children']
                applicant.child_care_costs =  serializer.data['child_care_costs']
                applicant.cars =  serializer.data['cars']
                applicant.loan_purpose = serializer.data['loan_purpose']
                applicant.save()
                applicant.loans.all().delete()
                for loan in serializer.data['loans']:
                    LoanOutstand.objects.create(
                        applicant=applicant,
                        lender=loan['lender'],
                        amount=loan['amount']
                    )
            return self.response(5, self.get_data(applicant))
        return self.error(serializer.errors)


class Step5(BaseCustomerStep):
    def get_data(self, applicant):
        return {
            'job_title': applicant.job_title,
            'employer_name': applicant.employer_name,
            'employer_address': applicant.employer_address,
            'nin': applicant.nin,
        }

    def get(self, request):
        applicant = self.get_applicant(request)
        return self.response(5, self.get_data(applicant))

    def post(self, request):
        applicant = self.get_applicant(request)
        serializer = CustomerStep5(data=request.data)
        if serializer.is_valid():
            applicant.job_title = serializer.data['job_title']
            applicant.employer_name = serializer.data['employer_name']
            applicant.employer_address = serializer.data['employer_address']
            applicant.nin = serializer.data.get('nin')
            applicant.save()
            return self.response(6, self.get_data(applicant))
        return self.error(serializer.errors)


class Step6(BaseCustomerStep):
    def get_data(self, applicant):
        return {
            'partner_income': applicant.partner_income,
            'partner_contrib': applicant.partner_contrib,
        }

    def get(self, request):
        applicant = self.get_applicant(request)
        return self.response(6, self.get_data(applicant))

    def post(self, request):
        applicant = self.get_applicant(request)
        serializer = CustomerStep6(data=request.data)
        if serializer.is_valid():
            applicant.partner_income = serializer.data['partner_income']
            applicant.partner_contrib = serializer.data['partner_contrib']
            applicant.save()
            return self.response(7, self.get_data(applicant))
        return self.error(serializer.errors)


class Step7(BaseCustomerStep):
    def get_data(self, applicant):
        return {
            'phone_mobile': applicant.phone_mobile,
        }

    def get(self, request):
        applicant = self.get_applicant(request)
        return self.response(7, self.get_data(applicant))

    def post(self, request):
        applicant = self.get_applicant(request)
        serializer = CustomerStep7(data=request.data)
        if serializer.is_valid():
            applicant.phone_mobile = serializer.data['phone_mobile']
            applicant.save()
            token = Cache().get_pin(applicant.id)
#            send_sms(applicant.phone_mobile, token)
            return self.response(8, self.get_data(applicant))
        return self.error(serializer.errors)


class Step8(BaseCustomerStep):
    def get_data(self, applicant):
        return {
            'phone_mobile': applicant.phone_mobile,
        }

    def get(self, request):
        applicant = self.get_applicant(request)
        return self.response(8, self.get_data(applicant))

    def post(self, request):
        applicant = self.get_applicant(request)
        serializer = CustomerStep8(data=request.data)
        if serializer.is_valid():
            if applicant.id == Cache().get(serializer.data['pin'], True):
                applicant.is_phone_verified = True
                applicant.save()
                return self.response(9, self.get_data(applicant))
            return self.error({'pin': 'wrong pin'})
        return self.error(serializer.errors)


def main(request, token):
    app_id = Cache().get(token, True)
    try:
        applicant = Applicant.objects.get(id=app_id)
    except Applicant.DoesNotExist:
        raise Http404
    return redirect('{}?code={}'.format(
        reverse('customer_step1'),
        applicant.access_token)
    )


def signature(request, token):
    app_id = Cache().get(token, True)
    try:
        applicant = Applicant.objects.get(id=app_id)
    except Applicant.DoesNotExist:
        raise Http404
    return redirect('{}?code={}'.format(
        reverse('customer_step3'),
        applicant.access_token)
    )
