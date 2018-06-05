from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect,reverse
from .forms import RegisterForm,LoginForm, BookForm, modifybookForm
from .models import User, Car, CarBooked
from django.contrib import messages
from passlib.hash import pbkdf2_sha256
from django.contrib.auth import authenticate, login as logg, logout as loggout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from datetime import date
from django.db.models import F

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

            carsbooked=CarBooked.objects.filter(model=id)
            print(carsbooked)
            print("lunghezzaa")
            print(len(carsbooked))
            if len(carsbooked) >0:
                cont=0
                try:
                    carbookedid = CarBooked.objects.latest('id')
                    print(carbookedid.id)

                    last=carbookedid.id+1
                    for i in range(1, last):
                        try:
                            print(i)
                            s=CarBooked.objects.filter(model=id).get(id=i)
                            print(s)
                            print("valutaA")
                            print(s.valuta(datainit=frombooked,datafine=tobooked))
                            c=s.valuta(datainit=frombooked,datafine=tobooked)
                            print("c:")
                            print(c)
                            if c == "In mezzo":
                                cont=cont+1
                                print("cont: ")
                                print(cont)
                                messages.error(request,"In questa data c'è già una prenotazione :(")
                                return redirect('details',id)
                        except:
                            print("pass")

                except:
                        print("pass2")
            else:
                pass

            newbook=CarBooked(frombooked=frombooked, tobooked=tobooked,place=place,note=note,model=cars)
            newbook.save()
            newbook.username.add(user)
            print("Non ancora")
            print(newbook.id)
            return HttpResponseRedirect('index')

    else:
        form = BookForm()


    cars=Car.objects.filter(id=id)
    print(id)
    carsbooked=CarBooked.objects.filter(model=id)
    print("username preno: %s"%carsbooked)

    return render(request,'detailscar.html',{'cars':cars,'carsbooked':carsbooked,'form':form})

@login_required
def modifybook(request,id):
    if request.method == 'POST':

        form = modifybookForm(request.POST)

        if form.is_valid():

            frombooked=form.cleaned_data['frombooked']
            tobooked=form.cleaned_data['tobooked']
            place=form.cleaned_data['place']
            note=form.cleaned_data['note']

            utente=request.user

            user=User.objects.get(username=utente)
            print(user)
            #print(u2)

            newbook=CarBooked.objects.get(id=id)
            newbook.frombooked=frombooked
            newbook.tobooked=tobooked
            newbook.note=note
            newbook.place=place
            print("save")
            newbook.save()
            return redirect('bookedbyme',id=id)
        else:
            return HttpResponse('non valido')

    else:
        carsbooked=CarBooked.objects.filter(id=id)
        for carbooked in carsbooked:
                carfromdate=carbooked.frombooked
                print(carfromdate)
                cartodate=carbooked.tobooked
                carboplace=carbooked.place
                carnote=carbooked.note

        form = modifybookForm(initial={'frombooked':carfromdate,'tobooked':cartodate,'place':carboplace,'note':carnote})
        print("ciooooooooooo")

    return render(request,'modifybook.html',{'form':form,'carsbooked':carsbooked})

def deletebook(request,id):
    CarBooked.objects.filter(id=id).delete()

    return redirect('index')

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
            password=form.cleaned_data['password']
            password2=request.POST['password2']
            if password == password2:
                user=form.save()
                user.set_password(user.password)
                user.save()
                messages.success(request,'Congratulation! Now you are registered correctly.')
            else:
                messages.error(request, 'Password doesn\'t match')
                return redirect('register')
        else:
            messages.error(request, 'This username is already used, choose another one')
            return redirect('register')
    else:
        form = RegisterForm()

    return render(request,'register.html', {'form':form})
