import datetime
from django.db import models    
from django.utils import timezone


class Questao(models.Model):
    testo_questao = models.CharField(max_length=200)
    data_publi = models.DateTimeField("Data de publicação")
    def __str__(self):
        return self.testo_questao
    def foiPublicado(self):
        return self.data_publi >= timezone.now() - datetime.timedelta(days=1)


class Escolha(models.Model):
    questao = models.ForeignKey(Questao, on_delete=models.CASCADE)
    texto_escolha = models.CharField(max_length=200)
    votos = models.IntegerField(default=0)
    def __str__(self):
        return self.texto_escolha