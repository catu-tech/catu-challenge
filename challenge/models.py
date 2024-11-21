from django.db import models

from django.utils.translation import gettext as _

class InvoiceStatus(models.TextChoices):
    ERROR = 'erro', _('Erro')
    SEND = 'enviado', _('Enviado')
    PROCESS = 'processando_autorizacao', _('Processando')
    NOT_AUTHORIZED = 'erro_autorizacao', _('Não autorizado')
    AUTHORIZED = 'autorizado', _('Autorizado')
    CANCELLED = 'cancelado', _('Cancelado')
    DENEGATED = 'denegado', _('Denegado')
    MANIFESTED = 'manifestado', _('Manifestado')

class Invoice(models.Model):

    ref = models.BigIntegerField(unique=True)

    data_emissao = models.DateField(blank=True, null=True)

    cnpj_emitente = models.CharField(max_length=255, blank=True, null=True)
    cpf_emitente = models.CharField(max_length=255, blank=True, null=True)
    inscricao_estadual_emitente = models.CharField(max_length=255, blank=True, null=True)

    cnpj_destinatario = models.CharField(max_length=255, blank=True, null=True)
    cpf_destinatario = models.CharField(max_length=255, blank=True, null=True)
    inscricao_estadual_destinatario = models.CharField(max_length=255, blank=True, null=True)

    status = models.CharField(choices=InvoiceStatus.choices, max_length=30, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

class InvoiceItem(models.Model):

    invoice = models.ForeignKey(Invoice, to_field='ref', on_delete=models.DO_NOTHING, null=True, blank=True)

    numero_item = models.CharField(max_length=255, blank=True, null=True)
    codigo_produto = models.CharField(max_length=255, blank=True, null=True)
    descricao = models.CharField(max_length=255, blank=True, null=True)
    codigo_ncm = models.CharField(max_length=255, blank=True, null=True)
    inclui_no_total = models.CharField(max_length=255, blank=True, null=True)

    cfop = models.CharField(max_length=255, blank=True, null=True)

    unidade_comercial = models.CharField(max_length=255, blank=True, null=True)
    quantidade_comercial = models.CharField(max_length=255, blank=True, null=True)
    valor_unitario_comercial = models.CharField(max_length=255, blank=True, null=True)

    icms_origem = models.CharField(max_length=255, blank=True, null=True)
    icms_situacao_tributaria = models.CharField(max_length=255, blank=True, null=True)
    pis_situacao_tributaria = models.CharField(max_length=255, blank=True, null=True)
    cofins_situacao_tributaria = models.CharField(max_length=255, blank=True, null=True)

    valor_frete = models.CharField(max_length=255, blank=True, null=True)
    valor_seguro = models.CharField(max_length=255, blank=True, null=True)
    valor_desconto = models.CharField(max_length=255, blank=True, null=True)