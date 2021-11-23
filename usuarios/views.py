from django.shortcuts import render, redirect, reverse


def cadastro(request):
    if request.method == 'POST':
        nome = request.POST['nome']
        email = request.POST['email']
        senha = request.POST['password']
        senha2 = request.POST['password2']
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
