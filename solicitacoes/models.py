from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
import uuid

def upload_sanitario(instance, filename):
    return f'protocolos/{instance.protocolo}/documento_sanitario.pdf'

def upload_meio_ambiente(instance, filename):
    return f'protocolos/{instance.protocolo}/documento_meio_ambiente.pdf'

def upload_bombeiro(instance, filename):
    return f'protocolos/{instance.protocolo}/documento_bombeiro.pdf'

def upload_pessoal(instance, filename):
    return f'protocolos/{instance.protocolo}/documento_pessoal.pdf'

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
        upload_to=upload_sanitario,
        validators=[
            FileExtensionValidator(
                allowed_extensions=['pdf']
            )
        ]
    )

    documento_meio_ambiente = models.FileField(
        upload_to=upload_meio_ambiente,
        validators=[
            FileExtensionValidator(
                allowed_extensions=['pdf']
            )
        ]
    )

    oficio_bombeiro = models.FileField(
        upload_to=upload_bombeiro,
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(
                allowed_extensions=['pdf']
            )
        ]
    )

    documento_pessoal = models.FileField(
        upload_to=upload_pessoal,
        blank=True,
        null=True
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

        campos_alterados = []

        for campo, nome_final in arquivos:

            arquivo = getattr(self, campo)

            if arquivo and arquivo.name:

                origem = arquivo.path

                destino = os.path.join(
                    pasta,
                    nome_final
                )

                if os.path.exists(origem):

                    os.replace(
                        origem,
                        destino
                    )

                    novo_caminho = f"protocolos/{self.protocolo}/{nome_final}"

                    setattr(
                        self,
                        campo,
                        novo_caminho
                    )

                    campos_alterados.append(campo)

        if campos_alterados:

            super().save(
                update_fields=campos_alterados
            )
def __str__(self):
    return f'{self.protocolo} - {self.nome_evento}'
