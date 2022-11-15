import imp
import qrcode
import random
import base64
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from numpy import require
from usuarios.forms import LoginForm, RegisterForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User
from usuarios.models import UserTOTP
import TOTP

# Create your views here.
def index(request):
    if 'username' in request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/usuarios/OTP_verify')
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
        if form.is_valid() & (not User.objects.filter(username=request.POST['username']).exists()):
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username = username, password = password)
            login(request, user)
            return redirect('./OTP_generator')
        elif (User.objects.filter(username=request.POST['username']).exists()):
            messages.success(request, 'Usuario ya registrado')
            return redirect('./register')
        else:
            messages.success(request, 'Contraseñas incorrectas')
            return redirect('./register')

    else:
        register_form=RegisterForm()
        context = {'register_form':register_form}

    return render(request, 'usuarios/register.html', context)

def log_out(request):
    logout(request)
    return redirect('/usuario/')

def introducir_token(request):

    context = {}

    if request.user.is_authenticated == False:
        redirect('/usuario')

    if request.method == 'POST':
        
        try:
            TOTPhash = UserTOTP.objects.get(user=request.user).user_hash_id
        except:
            context = {'error_message': 'Algo fue mal, contacta con el administrador'}
            return render(request, 'usuarios/OTPverify.html', context)

        
        code = TOTP.TOTPcodeFromUser(TOTPhash, "6")

        print(code)
        print(request.POST['OTPvalue'])

        if (code != request.POST['OTPvalue']):
            context = {'error_message': 'OTP code no valido. Quizás lo introdujiste demasiado tarde?'}
            return render(request, 'usuarios/OTPverify.html', context)


        return redirect('/usuario/success')

    return render(request, 'usuarios/OTPverify.html', context)

def verified(request):
    return HttpResponse("Tas logeao manin")

def createTOTPPasswd(request):

    key = random.randbytes(20)
    token = base64.b32encode(key).decode("utf-8")

    #UserTOTP.
    #TOTPhash = UserTOTP.objects.get(user=request.user).user_hash_id
    UserTOTP.objects.create(user=request.user, user_hash_id=token)

    qr_string = "otpauth://totp/WebExampleTOTP?secret=" + token +"&algorithm=SHA1&digits=6&period=30"

    context = {'html_img':qr_string}

    return render(request, 'usuarios/OTPgen.html', context)