from django.shortcuts import render,redirect
from .models import Product, Category
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import SignUpForm, UpdateUserForm, UpdatePasswordForm
from django import forms

def category_summary(request):
    categories = Category.objects.all()
    return render(request, 'category_summary.html', {"categories":categories})

def category(request,cat):
    #replace any hyphens with spaces
    cat = cat.replace('-', ' ')

    try:
        category = Category.objects.get(name=cat)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html',{'products':products,'category':category})
    except:
        messages.success(request, ('Invalid Category!'))
        return redirect('home')


def product(request,pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html',{'product':product})

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html',{'products':products})

def about(request):
    return render(request, 'about.html', {})

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("Logged in Successfully."))
            return redirect('home')
        else:
            messages.success(request, ("Loggin failed.Incorrect credentials."))
            return redirect('login')
    else:
        return render(request, 'login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, ("Logged out successfully."))
    return redirect('home')

def register_user(request):
    form = SignUpForm
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username,password=password)
            login(request, user)
            messages.success(request, ("You have registered successfully."))
            return redirect('home')
        else:
            messages.success(request, ("Registration unsuccessful."))
            return redirect('register')
    else:
        return render(request, 'register.html', {'form':form})

def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        form = UpdateUserForm(request.POST or None, instance=current_user)
        if form.is_valid():
            form.save()
            login(request, current_user)
            messages.success(request, ("User updated successfully."))
            return redirect('home')
        return render(request, 'update_user.html', {'form':form})
    else:
        messages.success(request, ("User Must be logged in to update information."))
        return redirect('login')
    
def update_password(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        if request.method == "POST":
            form = UpdatePasswordForm(current_user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, ("Password updated successfully."))
                login(request, current_user)
                return redirect('update_user')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                return redirect('update_password')
        else:
            form = UpdatePasswordForm(user=current_user)
            return render(request, 'update_password.html', {'form':form})
    else:
        messages.success(request, ("User Must be logged in to update password."))
        return redirect('login')

    
