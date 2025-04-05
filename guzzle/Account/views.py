import time
from django.shortcuts import render, redirect
from django.db import IntegrityError
from .application import AccountApplication
from django.contrib import messages

accountApplication = AccountApplication()

def signup(request):
    context = {'errorMessage': []}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')        

        try:            
            accountApplication.createAccount(username, password)
            accountApplication.login(request, username, password)
            accountApplication.setUserID(request.user.id)
            return redirect('home')

        except IntegrityError:
            context['errorMessage'].append('Username already exists')

    return render(request, 'signupPage.html', context)

def login(request):
    context = {'errorMessage': []}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        userExists = accountApplication.login(request, username, password)
        if userExists:
            accountApplication.setUserID(request.user.id)
            return redirect('home')
        else:
            context['errorMessage'].append('Account does not exist')

    return render(request, 'loginPage.html', context)

def signout(request):
    context = {}
    logoutSuccessful = accountApplication.logout(request)
    if logoutSuccessful:
        messages.success(request, 'Succsessfully signed out')
        time.sleep(1)
        return redirect('home')
    else:
        context['errorMessage'] = "Already signed out"    
    print(context)
    return render(request, 'signoutPage.html', context)