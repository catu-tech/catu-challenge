from rest_framework import viewsets
from rest_framework.decorators import action

from rest_framework.response import Response

from .models import Invoice
from .serializers import InvoiceSerializer

from rest_framework import status

class ChallengeViewset(viewsets.ViewSet):
    @action(detail=False, methods=["get"], url_path="list/all")
    def list_all(self, request):
        invoices = Invoice.objects.all()
        serializer = InvoiceSerializer(invoices, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # Pode adicionar todo o código aqui mesmo