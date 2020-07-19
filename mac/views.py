from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User, auth


# Create your views here.
def index(request):
    return render(request, 'index.html')


def registration(request):
    if request.method == 'POST':
        print(request)
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username taken please try again with another Username')
                return redirect('/registration')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email taken please try again with different Email Address')
                return redirect('/registration')
            else:
                user = User.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username,
                            password=password1)
                user.save()
                print('User Created')
                return redirect('/login')

        else:
            messages.info(request, 'Please Check both Passwords, Passwords not matching')
            return redirect('/registration')
        return redirect('/registration')
    else:

        return render(request, 'registration.html')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            print('Loged in')
            return redirect('/shop')

        else:
            messages.info(request, "Invalid Credentials")
            return redirect('/login')
    else:
        return render(request, 'login.html')
def logout(request):
    auth.logout(request)
    return redirect('/')