from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from receitas.models import Receita


def cadastro(request):
    if request.method == 'POST':
        nome = request.POST['nome']
        email = request.POST['email']
        senha = request.POST['password']
        senha2 = request.POST['password2']
        if not nome.strip():
            messages.error(request, 'O campo nome não pode ficar vazio')
            return redirect(reverse('cadastro'))
        if not email.strip():
            messages.error(request, 'Email não pode ser vazio')
            return redirect(reverse('cadastro'))
        if senha2 != senha:
            messages.error(request, 'As senhas não conferem')
            return redirect(reverse('cadastro'))
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email já cadastrado')
            return redirect(reverse('cadastro'))

        user = User.objects.create_user(username=nome, email=email, password=senha)
        user.save()
        messages.success(request, 'Usuário cadastrado com sucesso!')
        return redirect(reverse('login'))
    else:
        return render(request, 'usuarios/cadastro.html')


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        senha = request.POST['password']
        if email == '' or senha == '':
            messages.error(request, 'Email ou senha não pode ser vazio')
            return redirect(reverse('login'))
        print(email, senha)
        if User.objects.filter(email=email).exists():
            nome = User.objects.get(email=email).values_list('username', flat=True).get()
            user = authenticate(request, username=nome, password=senha)
            if user is not None:
                login(request, user)
                return redirect(reverse('dashboard'))

    return render(request, 'usuarios/login.html')


def logout(request):
    logout(request)
    return redirect(reverse('login'))


def dashboard(request):
    if request.user.is_authenticated:
        id = request.user.id
        receitas = Receita.objects.order_by('-date_receita').filter(pessoa=id)
        dados = {'receitas': receitas}
        return render(request, 'usuarios/dashboard.html', dados)
    else:
        return redirect(reverse('login'))


def cria_receita(request):
    if request.method == 'POST':
        nome_receita = request.POST['nome_receita']
        ingredientes = request.POST['ingredientes']
        modo_preparo = request.POST['modo_preparo']
        tempo_preparo = request.POST['tempo_preparo']
        rendimento = request.POST['rendimento']
        categoria = request.POST['categoria']
        foto_receita = request.FILES['foto_receita']
        user = get_object_or_404(User, pk=request.user.id)
        receita = Receita.objects.create(pessoa=user, nome_receita=nome_receita, ingredientes=ingredientes,
                                         modo_preparo=modo_preparo, tempo_preparo=tempo_preparo, rendimento=rendimento,
                                         categoria=categoria, foto_receita=foto_receita)
        receita.save()
        return redirect(reverse('dashboard'))
    else:
        return render(request, 'usuarios/cria_receita.html')
