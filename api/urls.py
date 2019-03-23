from django.conf.urls import url, include

from api.views import AuthenticationView
from api.views import NewOrderView
from api.views import UpdateOrderView
from api.views import MyOrdersView
from api.views import StoreOrdersView
from api.views import CodeInfoView

urlpatterns = [
    url(r'^auth/$', AuthenticationView.as_view(), name='api_auth'),
    url(r'^new_order/$', NewOrderView.as_view(), name='api_new_order'),
    url(r'^update_order/$', UpdateOrderView.as_view(), name='api_update_order'),
    url(r'^my_orders/$', MyOrdersView.as_view(), name='api_my_orders'),
    url(r'^store_orders/$', StoreOrdersView.as_view(), name='api_store_orders'),
    url(r'^code_info/$', CodeInfoView.as_view(), name='api_code_info')
]
