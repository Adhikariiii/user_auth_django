from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import auth, messages
from .models import Feature


# Create your views here.

def index(request):
    feature = Feature.objects.all()
    return render(request, 'index.html', {'features': feature} )
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Sorry the email already exists ')
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                 messages.info(request, 'sorry the username already exists')
                 return redirect('register')
            else:
                 user = User.objects.create_user(username=username, email=email, password=password)
                 user.save()
                 return redirect('login')
        else:
            messages.info(request, 'Password did not matched')
            return redirect('register')

    else:
        return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Invalid credentails')
            return redirect('login')

    return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')