from tkinter.ttk import Style
from turtle import onclick
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, ButtonHolder, HTML


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML('<label for="username">Usuario:</label><br> <input type="text" id="username" name="username" required><br>'),
            HTML('<label for="password">Contraseña:</label><br> <input type="password" id="password" name="password" required><br><br>'),
            ButtonHolder(
                Submit('login', 'Login', css_class='formbutton')
            )
        )

class RegisterForm(forms.Form, UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        
        self.helper = FormHelper()
        self.helper.form_id = 'id-registerForm'
        self.helper.form_class = 'form-group'
        self.helper.form_method = 'post'
        self.helper.form_action = ''
        self.helper.add_input(Submit('registrar', 'Registrar', css_class='formbutton'))

        # self.helper.layout = Layout(
        #     HTML('<label for="username">Usuario:</label><br> <input type="text" id="username" name="login" required><br>'),
        #     HTML('<label for="password">Contraseña:</label><br> <input type="password" id="password" name="password" required><br>'),
        #     HTML('<label for="confirm_password">Confirmar contraseña:</label><br> <input type="password" id="confirm_password" name="confirm_password" required><br>'),
        #     ButtonHolder(
        #         Submit('login', 'Login', css_class='formbutton')
        #     )
        # )

    
