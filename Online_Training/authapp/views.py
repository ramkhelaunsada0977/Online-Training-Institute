from django.shortcuts import render,redirect
from django.contrib import messages
import re
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.views.generic import View
from django.template.loader import render_to_string
# from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
# from .utils import TokenGenerator,generate_token
# from django.utils.encoding import force_bytes,force_text,DjangoUnicodeDecodeError
# from django.core.mail import EmailMessage
# from django.conf import settings
from authapp.models import Contact
# Create your views here.
def signup(request):
    flag= 0
    if request.method=="POST":
        name=request.POST['name']
        email=request.POST['email']
        password=request.POST['pass1']
        confirm_password=request.POST['pass2']
        if password != confirm_password:
            messages.warning(request,"Password is not matching")
            return redirect('/auth/signup/')
        if len(password)<=8:
            messages.warning(request,"Passwrod must be atleast 8 character")
            return redirect('/auth/signup/')
        elif not re.search("[a-z]", password):
            flag= -1
        elif not re.search("[A-Z]", password):
            flag= -1
        elif not re.search("[0-9]", password):
            flag= -1
        elif not re.search("[_$@#%^*()-]", password):
            flag= -1
        else:
            pass
        if(flag==0):
            try:
                if User.objects.get(username=email):
                    messages.info(request,"Email is Taken")
                    return redirect('auth/signup/')
            except Exception as identifier:
                pass
            user =User.objects.create_user(email,email,password)
            user.first_name=name
            user.is_active=False

            # email_subject="Activate Your Account"
            # message=render_to_string('activate.html',{
            #     'user':user,
            #     'domain':'127.0.0.1:8000',
            #     'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            #     'token':generate_token.make_token(user)
            # })
            # email_message= EmailMessage(email_subject,message,settings)
            # EMAIL_HOST_USER,[email]
            # email_message.send()
            # message.success(request,f"{message}")
            user.save()
            messages.success(request, "Signup Success please login")
            return redirect('/auth/login/')
        else:
            messages.error(request, "Password is not valid")
            return redirect('/auth/signup/')
    return render(request, 'signup.html')

def handleLogin(request):
    if request.method=="POST":
        username=request.POST['email']
        userpassword=request.POST['pass1']
        myuser=authenticate(username=username,password=userpassword)
        if myuser is not None:
            login(request,myuser)
            messages.success(request,"Login Success")
            return redirect('/')
        else:
            messages.error(request,"Invalid Credential")
            return redirect('/auth/login/')
    return render(request, 'login.html')

def handleLogout(request):
    logout(request)
    messages.success(request,"Logout success")
    return render(request, 'login.html')