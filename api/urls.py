from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import *

urlpatterns = [
    path("orders/send", SendOrder.as_view(), name='orders_send')
]

urlpatterns = format_suffix_patterns(urlpatterns)
