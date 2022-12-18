from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages


def register(request):   
    if request.method == "POST" :
        firstname = request.POST['f_name']
        lastname = request.POST['l_name']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password : 
            if User.objects.filter(username = username).exists():
                messages.info(request, "Username already taken")
                return redirect("register")
            elif User.objects.filter(email = email).exists():
                messages.info(request, "Email already in use")
                return redirect("register")
            else :
                user = User.objects.create_user(username, email, password)
                user.first_name, user.last_name = firstname, lastname
                user.save()
                auth.login(request, user)
                return redirect("/main/")
        else :
            messages.info(request, 'Password not matched!')
            return redirect("register")
    return render(request, "accounts/register.html")



def login(request):
    form_name = request.POST.get('form_name')
    if request.method == "POST":
        if form_name == 'admin_form':
            email = request.POST['admin_email']
            password = request.POST['admin_password']
            username = User.objects.filter(email=email)[0].username
            user = auth.authenticate(request, username=username, password=password)
            if user:
                auth.login(request, user)
                return redirect("/main/")
            else:           
                return render(request, "accounts/login.html")
        elif form_name == 'stuff_form':
            email = request.POST['stuff_email']
            password = request.POST['stuff_password']
            username = User.objects.filter(email=email)[0].username
            user = auth.authenticate(request, username=username, password=password)
            if user:
                auth.login(request, user)
                return redirect("/main/")
            else:           
                return render(request, "accounts/login.html")
    return render(request, "accounts/login.html")



def logout(request):
    auth.logout(request)
    return redirect("/main/")
