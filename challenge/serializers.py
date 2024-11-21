from rest_framework import serializers

from .models import Invoice, InvoiceItem

class InvoiceSerializer(serializers.ModelSerializer):

    itens = serializers.SerializerMethodField('get_itens')

    def get_itens(self, obj):
        ret = []
        itens = InvoiceItem.objects.filter(invoice=obj.ref)
        if len(itens):
            ret = InvoiceItemSerializer(itens, many=True).data
        return ret
    
    class Meta:
        model = Invoice
        fields = '__all__'

class InvoiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceItem
        fields = '__all__'