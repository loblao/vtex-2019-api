from django.conf.urls import url, include

from api.views import AuthenticationView

urlpatterns = [
    url(r'^auth/$', AuthenticationView.as_view(), name='api_auth'),
]
