from django.shortcuts import render, redirect, reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from apps.receitas.models import Receita


def cadastro(request):
    """Cadastra um novo usuário"""
    if request.method == 'POST':
        nome = request.POST['nome']
        email = request.POST['email']
        senha = request.POST['password']
        senha2 = request.POST['password2']
        if campo_vazio(nome):
            messages.error(request, 'O campo nome não pode ficar vazio')
            return redirect(reverse('cadastro'))
        if campo_vazio(email):
            messages.error(request, 'Email não pode ser vazio')
            return redirect(reverse('cadastro'))
        if senhas_nao_sao_iguais(senha, senha2):
            messages.error(request, 'As senhas não conferem')
            return redirect(reverse('cadastro'))
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email já cadastrado')
            return redirect(reverse('cadastro'))
        if User.objects.filter(username=nome).exists():
            messages.error(request, 'Usuário já cadastrado')
            return redirect(reverse('cadastro'))

        user = User.objects.create_user(username=nome, email=email, password=senha)
        user.save()
        messages.success(request, 'Usuário cadastrado com sucesso!')
        return redirect(reverse('login'))
    else:
        return render(request, 'usuarios/cadastro.html')


def login(request):
    """Realiza o login do usuário"""
    if request.method == 'POST':
        email = request.POST['email']
        senha = request.POST['password']
        if campo_vazio(email) or campo_vazio(senha):
            messages.error(request, 'Email ou senha não pode ser vazio')
            return redirect(reverse('login'))
        if User.objects.filter(email=email).exists():
            nome = User.objects.get(email=email).values_list('username', flat=True).get()
            user = authenticate(request, username=nome, password=senha)
            if user is not None:
                login(request, user)
                return redirect(reverse('dashboard'))

    return render(request, 'usuarios/login.html')


def logout(request):
    """Realiza o logout do usuário"""
    logout(request)
    return redirect(reverse('login'))


def dashboard(request):
    """Página inicial do usuário"""
    if request.user.is_authenticated:
        id = request.user.id
        receitas = Receita.objects.order_by('-date_receita').filter(pessoa=id)
        dados = {'receitas': receitas}
        return render(request, 'usuarios/dashboard.html', dados)
    else:
        return redirect(reverse('login'))


def campo_vazio(campo):
    """Verifica se o campo está vazio"""
    return not campo.strip()


def senhas_nao_sao_iguais(senha, senha2):
    """Verifica se as senhas não são iguais"""
    return senha != senha2
