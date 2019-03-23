# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.utils import timezone

from django.views import View
from django.http import JsonResponse

from api.models import Store
from api.models import APIUser
from api.models import SessionToken
from api.models import OrderInfo
from api.models import STATUS_PEN

import datetime
import os


@method_decorator(csrf_exempt, name='dispatch')
class AuthenticationView(View):
    def post(self, request, *args, **kwargs):
        # TODO: validate input
        username = request.POST.get('username')
        password = request.POST.get('password')

        response = {'success': False, 'reason': 'auth'}

        # Authenticate
        try:
            u = APIUser.objects.get(username=username)
            if u.check_password(password):
                # Generate new token
                t = SessionToken(user=u)
                t.value = os.urandom(16).encode('hex')
                t.expiration = timezone.now() + datetime.timedelta(hours=settings.SESSION_TOKEN_EXPIRATION)
                t.save()

                response = {'success': True, 'is_staff': u.is_staff,
                            'token': t.value}

        except APIUser.DoesNotExist:
            pass

        return JsonResponse(response)


@method_decorator(csrf_exempt, name='dispatch')
class NewOrderView(View):
    def post(self, request, *args, **kwargs):
        # TODO: validate input
        username = request.POST.get('username')
        name = request.POST.get('name')

        try:
            store_token = request.POST.get('store_token')
            store = Store.objects.get(api_token=store_token)

        except Store.DoesNotExist:
            response = {'success': False, 'reason': 'unknown store'}
            return JsonResponse(response)

        desc = request.POST.get('desc')
        link = request.POST.get('link')
        price = float(request.POST.get('price'))
        status = int(request.POST.get('status', STATUS_PEN))
        payment_info = request.POST.get('payment_info')
        seller = request.POST.get('seller')
        expected_date = request.POST.get('expected_date')
        expected_date = datetime.datetime.strptime(expected_date, '%Y-%m-%d %H:%M:%S')

        try:
            u = APIUser.objects.get(username=username)

            order = OrderInfo(user=u, name=name, store=store,
                              price=price, status=status,
                              expected_date=expected_date,
                              payment_info=payment_info,
                              seller=seller, link=link,
                              desc=desc)
            order.code = os.urandom(16).encode('hex')
            order.save()

            response = {'success': True, 'code': order.code}

        except APIUser.DoesNotExist:
            response = {'success': False, 'reason': 'unknown user'}

        return JsonResponse(response)


@method_decorator(csrf_exempt, name='dispatch')
class UpdateOrderView(View):
    def post(self, request, *args, **kwargs):
        order_code = request.POST.get('code')

        try:
            store_token = request.POST.get('store_token')
            store = Store.objects.get(api_token=store_token)

        except Store.DoesNotExist:
            response = {'success': False, 'reason': 'unknown store'}
            return JsonResponse(response)

        try:
            order = OrderInfo.objects.get(code=order_code, store=store)

            # Update with given info
            if 'name' in request.POST:
                order.name = request.POST['name']

            if 'link' in request.POST:
                order.link = request.POST['link']

            if 'status' in request.POST:
                order.status = request.POST['status']

            if 'payment_info' in request.POST:
                order.payment_info = request.POST['payment_info']

            if 'seller' in request.POST:
                order.seller = request.POST['seller']

            if 'expected_date' in request.POST:
                expected_date = request.POST['expected_date']
                order.expected_date = datetime.datetime.strptime(expected_date, '%Y-%m-%d %H:%M:%S')

            order.save()
            response = {'success': True}

        except OrderInfo.DoesNotExist:
            response = {'success': False, 'reason': 'unknown order'}

        return JsonResponse(response)
