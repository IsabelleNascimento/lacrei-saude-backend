from django.db import models


class Profissional(models.Model):
    nome_social = models.CharField(max_length=255)
    profissao = models.CharField(max_length=100)
    endereco = models.CharField(max_length=255)
    contato = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.nome_social} ({self.profissao})"


class Consulta(models.Model):
    data = models.DateTimeField()
    
    profissional = models.ForeignKey(
        Profissional, 
        on_delete=models.CASCADE, 
        related_name='consultas'
    )

    def __str__(self):
        return f"Consulta em {self.data.strftime('%d/%m/%Y %H:%M')} com {self.profissional.nome_social}"
