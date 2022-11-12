import imp
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from numpy import require
from usuarios.forms import LoginForm, RegisterForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
#from models import Usuario
import TOTP


from usuarios.models import Usuario

# Create your views here.
def index(request):
    if 'username' in request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/conciertos/log_in')
        else:
            messages.success(request, 'Credenciales incorrectas')
            return redirect('./')
    login_form=LoginForm()
    context = {'login_form':login_form}

    return render(request, 'usuarios/index.html', context)

def register(request):
    context = {}
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username = username, password = password)
            login(request, user)
            return redirect('/conciertos/log_in')

    else:
        register_form=RegisterForm()
        context = {'register_form':register_form}

    return render(request, 'usuarios/register.html', context)

def log_out(request):
    logout(request)
    return redirect('/usuario/')

def introducir_token(request):

    if request.user.is_authenticated == False:
        redirect('/usuario')
    if request.method == 'POST':
        TOTP.generateTOTP()
        print(request.POST['OTPvalue'])

    return render(request, 'usuarios/OTPverify.html')