from django.db import models
from django.utils import timezone



class Predio(models.Model):
   nome = models.CharField(max_length=200)

   def __str__(self):
      return self.nome

class Chave(models.Model):
   sala = models.CharField(max_length=20)
   cod_RFID = models.IntegerField()
   descricao= models.CharField(max_length=50)
   emprestada = models.BooleanField(default=False)
   predio = models.ForeignKey(Predio, on_delete=models.CASCADE)
   portaria = models.ForeignKey('auth.User', default=None, on_delete=models.CASCADE) # usuario que emprestou

   def __str__(self):
      return self.descricao + ' no Prédio de ' + str(self.predio) + ' - cópia da ' + str(self.portaria.first_name)
   
class Pessoa(models.Model):
   nome = models.CharField(max_length=200)
   CPF = models.IntegerField()
   vinculo = models.CharField(max_length=200)
   cod_RFID = models.IntegerField()

   def __str__(self):
      return self.nome

class Emprestimo(models.Model):
   data_Retirada = models.DateTimeField(default=timezone.now)
   data_Entrega = models.DateTimeField(blank=True, null=True)
   chave = models.ForeignKey(Chave, on_delete=models.CASCADE)
   pessoa = models.ForeignKey(Pessoa, on_delete=models.CASCADE)
   

   def __str__(self):
      return str(self.pessoa) + " - " + str(self.chave) 
     
   





 