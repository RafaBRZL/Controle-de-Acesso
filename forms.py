from django import forms

class FormLogin(forms.Form):
   usuario = forms.CharField(label='Usuário', max_length=40)
   senha = forms.CharField(widget=forms.PasswordInput, min_length=4, max_length=20)

class FormEmprestimo(forms.Form):
   codigo = forms.CharField(label='Código', max_length=10, widget=forms.TextInput(attrs={'autofocus': True}))
