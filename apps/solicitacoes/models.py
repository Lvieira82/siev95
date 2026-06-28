
import uuid
import os
from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User
from django.conf import settings

def pasta_protocolo(instance, filename):

    protocolo = instance.protocolo

    if not protocolo:
        protocolo = "SEM_PROTOCOLO"

    return os.path.join(
        protocolo,
        filename
    )
def gerar_protocolo_unico():

    while True:

        protocolo = uuid.uuid4().hex[:8].upper()

        if not Solicitacao.objects.filter(
            protocolo=protocolo
        ).exists():
            return protocolo
def pasta_opo(instance, filename):

    protocolo = instance.protocolo or "SEM_PROTOCOLO"

    return os.path.join(
        "protocolos",
        protocolo,
        "opo",
        filename
    )
class Solicitacao(models.Model):
    

    STATUS = [
        ('PENDENTE', 'Pendente'),
        ('APROVADO', 'Aprovado'),
        ('REJEITADO', 'Rejeitado'),
    ]

    parecer_operacional = models.TextField(
        blank=True,
        null=True
    )

    aprovado_por = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    data_aprovacao = models.DateTimeField(
        blank=True,
        null=True
    )

    protocolo = models.CharField(
        max_length=20,
        unique=True,
        blank=True
    )

    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    nome_evento = models.CharField(
        max_length=200
    )

    solicitante = models.CharField(
        max_length=200
    )

    cpf = models.CharField(
    max_length=14,
    blank=True,
    null=True
    )
    
    numero_opo = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )

    efetivo_opo = models.TextField(
        blank=True,
        null=True,
        default="01 (uma) Guarnição a critério do Coordenador de Área. Modalidade: Patrulhamento. Processo: Motorizado."
    )

    comandante_opo = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        default="HELIO NERY DOS SANTOS JUNIOR - CAP PM, Mat. 30581994"
    )

    opo_pdf = models.FileField(
        upload_to=pasta_opo,
        blank=True,
        null=True
    )

    email = models.EmailField()

    telefone = models.CharField(
        max_length=20
    )

    data_evento = models.DateField()

    hora_inicio = models.TimeField()

    hora_fim = models.TimeField()

    local = models.TextField()

    publico_estimado = models.IntegerField()

    observacoes = models.TextField(
        blank=True
    )

    documento_sanitario = models.FileField(
        upload_to="temp/",
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(
                allowed_extensions=["pdf"]
            )
        ]
    )

    documento_meio_ambiente = models.FileField(
        upload_to="temp/",
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(
                allowed_extensions=["pdf"]
            )
        ]
    )

    oficio_bombeiro = models.FileField(
        upload_to="temp/",
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(
                allowed_extensions=["pdf"]
            )
        ]
    )

    
    assinado_por = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    data_assinatura = models.DateTimeField(
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default='PENDENTE'
    )

    criado_em = models.DateTimeField(
        auto_now_add=True
    )




    def save(self, *args, **kwargs):

        novo = self.pk is None

        if not self.protocolo:

            self.protocolo = gerar_protocolo_unico()

        super().save(*args, **kwargs)

        if novo:

            pasta = os.path.join(
                settings.MEDIA_ROOT,
                "protocolos",
                self.protocolo
            )

            os.makedirs(
                pasta,
                exist_ok=True
            )

            arquivos = [
                ("documento_sanitario", "documento_sanitario.pdf"),
                ("documento_meio_ambiente", "documento_meio_ambiente.pdf"),
                ("oficio_bombeiro", "oficio_bombeiro.pdf"),
            ]

            alterou = False

            for campo, nome_final in arquivos:

                arquivo = getattr(self, campo)

                if arquivo:

                    origem = arquivo.path

                    destino = os.path.join(
                        pasta,
                        nome_final
                    )

                    if origem != destino:

                        if os.path.exists(origem):

                            os.replace(
                                origem,
                                destino
                            )

                            setattr(
                                self,
                                campo,
                                f"protocolos/{self.protocolo}/{nome_final}"
                            )

                            alterou = True

            if alterou:

                super().save(
                    update_fields=[
                        "documento_sanitario",
                        "documento_meio_ambiente",
                        "oficio_bombeiro",
                    ]
                )

    def __str__(self):

            return self.nome_evento
        
    
