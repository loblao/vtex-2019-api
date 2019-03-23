# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.utils import timezone

from django.views import View
from django.http import JsonResponse

from api.models import APIUser
from api.models import SessionToken

import datetime
import os


@method_decorator(csrf_exempt, name='dispatch')
class AuthenticationView(View):
    def post(self, request, *args, **kwargs):
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
