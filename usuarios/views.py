from django.shortcuts import render, redirect, reverse
from django.contrib.auth.models import User


def cadastro(request):
    if request.method == 'POST':
        nome = request.POST['nome']
        email = request.POST['email']
        senha = request.POST['password']
        senha2 = request.POST['password2']
        if not nome.strip():
            print('Nome não pode ser vazio')
            return redirect(reverse('cadastro'))
        if not email.strip():
            print('Email não pode ser vazio')
            return redirect(reverse('cadastro'))
        if senha2 != senha:
            print('Senhas não conferem')
            return redirect(reverse('cadastro'))
        if User.objects.filter(email=email).exists():
            print('Email já cadastrado')
            return redirect(reverse('cadastro'))

        user = User.objects.create_user(username=nome, email=email, password=senha)
        user.save()
        print('Usuário cadastrado com sucesso!')
        return redirect(reverse('login'))
    else:
        return render(request, 'usuarios/cadastro.html')


def login(request):
    return render(request, 'usuarios/login.html')


def logout(request):
    pass


def dashboard(request):
    pass
