from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect,reverse
from .forms import RegisterForm,LoginForm, BookForm
from .models import User, Car, CarBooked
from django.contrib import messages
from passlib.hash import pbkdf2_sha256
from django.contrib.auth import authenticate, login as logg, logout as loggout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required

@login_required
def details(request,id):

    if request.method == 'POST':

        form = BookForm(request.POST)

        if form.is_valid():
            cars=Car.objects.get(id=id)
            print(cars)
            frombooked=form.cleaned_data['frombooked']
            tobooked=form.cleaned_data['tobooked']
            place=form.cleaned_data['place']
            note=form.cleaned_data['note']

            utente=request.user

            user=User.objects.get(username=utente)
            print(user)
            #print(u2)
            if  CarBooked.objects.filter(frombooked=frombooked,tobooked=tobooked):
                return HttpResponse("data già presente")
            else:
                newbook=CarBooked(frombooked=frombooked, tobooked=tobooked,place=place,note=note,model=cars,username=user)
                newbook.save()
            return HttpResponseRedirect('index')

    else:
        form = BookForm()
    cars=Car.objects.filter(id=id)
    print(id)
    carsbooked=CarBooked.objects.filter(model=id)
    return render(request,'detailscar.html',{'cars':cars,'carsbooked':carsbooked,'form':form})

@login_required
def index(request):
    cars=Car.objects.all()
    u=request.user.id
    print("u: ")
    print(u)

    carsbooked=CarBooked.objects.filter(username=u)
    return render(request,'index.html',{'cars':cars,"utente":request.user,'carsbooked':carsbooked})

@login_required
def bookedbyme(request,id):
    carsbooked=CarBooked.objects.filter(id=id)
    print(carsbooked)

    return render(request, 'bookedbyme.html',{'carsbooked':carsbooked})

@login_required
def aboutme(request):
    id=request.user.id
    print(id)
    user=User.objects.filter(id=id)

    return render(request, 'aboutme.html',{'user':user})

def authss(username=None, password=None):
    try:
        user = User.objects.get(username=username)
        if user.check_password(password):
            return user
    except User.DoesNotExist:
        return None

def login(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:

        if request.method == 'POST':

                username = request.POST.get('username')
                raw_password = request.POST.get('password')
                print(username)
                print(raw_password)
                user = authenticate(username=username, password=raw_password)
                if user:
                    if user.is_active:
                        print(user)
                        logg(request, user)
                        return redirect('index')
                    else:
                        return HttpResponse("disabled")
                else:
                    messages.error(request, 'Invalid credentials..')
                    return redirect('login')

        else:
            form = LoginForm()

    return render(request,'login.html', {'form':form})

def logout(request):
    loggout(request)
    return redirect('login')

def register(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            print(username)
            user = User.objects.filter(username=username)
            user=form.save()
            user.set_password(user.password)
            user.save()
        else:
            messages.error(request, 'This username is already used, choose another one')
            return redirect('register')



            return redirect('index')

    else:
        form = RegisterForm()

    return render(request,'register.html', {'form':form})
