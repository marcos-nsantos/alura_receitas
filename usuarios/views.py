from django.shortcuts import render, redirect, reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


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
    if request.method == 'POST':
        email = request.POST['email']
        senha = request.POST['password']
        if email == '' or senha == '':
            print('Os campos não podem fica vazios')
            return redirect(reverse('login'))
        print(email, senha)
        if User.objects.filter(email=email).exists():
            nome = User.objects.get(email=email).values_list('username', flat=True).get()
            user = authenticate(request, username=nome, password=senha)
            if user is not None:
                login(request, user)
                print('Usuário logado com sucesso!')
                return redirect(reverse('dashboard'))

    return render(request, 'usuarios/login.html')


def logout(request):
    logout(request)
    return redirect(reverse('login'))


def dashboard(request):
    if request.user.is_authenticated:
        return render(request, 'usuarios/dashboard.html')
    else:
        return redirect(reverse('login'))
