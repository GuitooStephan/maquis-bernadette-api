import logging

from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import generics
from rest_framework import (
    views, status
)

from scheduler.tasks import send_order

logger = logging.getLogger(__name__)

class SendOrder( views.APIView ):
    def post( self, request, format=None ):
        try:
            data = request.data.copy()
            send_order.delay( data )
            return Response( { "message": "Order sent" }, status=status.HTTP_200_OK )
        except Exception as e:
            logger.exception('[EXCEPTION] {}'.format(str(e)))
            return Response(
                { 'details': str(e) },
                status.HTTP_500_INTERNAL_SERVER_ERROR
            )


