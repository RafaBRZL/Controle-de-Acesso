from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Chave
from .models import Emprestimo
from .models import Pessoa
from .forms import FormLogin
from django.contrib.auth import authenticate, login, logout
from .forms import FormEmprestimo
from django.utils import timezone
def fazer_login(request):
   if request.method == 'POST':
       form = FormLogin(request.POST)
       if form.is_valid():
          usuario = form.cleaned_data['usuario']
          senha = form.cleaned_data['senha']
          user = authenticate(request, username=usuario, password=senha) # retorna None se o usuário não for encontrado
          if user is not None:
             login(request, user)
             messages.success(request, "Seja bem vindo " + user.first_name + "!")
             return HttpResponseRedirect("/controleacesso/")
          else:
             messages.error(request, "Usuário ou senha incorreto. Tente de novo.")
       else:
          messages.error(request, "Preencha corretamente o formulário")
   else:
      form = FormLogin()
          
   contexto = {"form": form}
   return render(request, 'controleacesso/login.html', contexto)

def fazer_logout(request):
   logout(request)
   return HttpResponseRedirect("/controleacesso/")
   


def index(request):
   if not request.user.is_authenticated:
      return HttpResponseRedirect('/controleacesso/login')
   form = FormEmprestimo()
   contexto = {"form": form, "titulo": "Aproxime a tag da chave para devolver ou retirar"}
   return render(request, 'controleacesso/index.html', contexto)

def listar(request):
   if not request.user.is_authenticated:
      messages.error(request, "Você precisa estar logado para acessar esta área.")
      return HttpResponseRedirect('/controleacesso/login')
    
   lista_chaves = Chave.objects.all()
   contexto = {'lista_chaves': lista_chaves}
   return render(request, 'controleacesso/listar.html', contexto)

def ver_chave(request, id):
   if not request.user.is_authenticated:
      messages.error(request, "Você precisa estar logado para acessar esta área.")
      return HttpResponseRedirect('/controleacesso/login') 
   
   c = Chave.objects.get(id=id)
   lista_emprestimos = c.emprestimo_set.all()
   contexto = {"c":c, 'lista_emprestimos':lista_emprestimos}
   return render(request, 'controleacesso/chave.html', contexto)

def avaliar_codigo(request):
   if not request.user.is_authenticated:
      messages.error(request, "Você precisa estar logado para acessar esta área.")
      return HttpResponseRedirect('/controleacesso/login')

   # encontrando código do formulário
   form = FormEmprestimo(request.POST)
   if form.is_valid():
      codigo = int(form.cleaned_data['codigo'])

   else:
      messages.error(request, "Erro ao avaliar código")
      return HttpResponseRedirect('/controleacesso/')
      
   # verificando se o código é uma chave
   
   lista_chaves = Chave.objects.filter(cod_RFID = codigo)
   if len(lista_chaves) > 0:
      chave = lista_chaves[0]
      if chave.emprestada:
         chave.emprestada = False
         chave.save()
         emprestimos = chave.emprestimo_set.filter(data_Entrega__isnull = True)
         e = Emprestimo.objects.get(id = emprestimos[0].id)
         e.data_Entrega = timezone.now()
         e.save()
         messages.success(request, "A chave " + str(chave) + " foi devolvida com sucesso.")
      else:
         messages.info(request, "Retirando a chave " + str(chave) )
         form = FormEmprestimo() 
         contexto = {"form": form, "id_chave": chave.id, "titulo": "Aproxime o crachá para confirmar o empréstimo"}
         return render(request, 'controleacesso/index.html', contexto)
      
   return HttpResponseRedirect('/controleacesso/')
   
def solicitar_pessoa(request, id_chave):
   if request.method == 'POST':
       form = FormEmprestimo(request.POST)
       if form.is_valid():
         codigo = int(form.cleaned_data['codigo'])
       else:
         messages.error(request, "Erro ao avaliar código")
         return HttpResponseRedirect('/controleacesso/')
       
       # buscado chave

       chave = Chave.objects.get(id = id_chave)

       # buscando pessoa

       lista_pessoas = Pessoa.objects.filter(cod_RFID = codigo)
       if len(lista_pessoas) > 0:
          pessoa = lista_pessoas[0]
          chave.emprestada = True
          chave.save()
          e = Emprestimo(chave = chave, pessoa = pessoa)
          e.save()

          messages.success(request, str(chave) + " Emprestada para " + str(pessoa))
          return HttpResponseRedirect('/controleacesso/')
       else:
          messages.error(request, "Pessoa não encontrada.")
          return HttpResponseRedirect('/controleacesso/')

   else:
      return HttpResponseRedirect('/controleacesso/')
      