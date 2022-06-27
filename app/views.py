
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login as loginuser, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from app.forms import TODOForms
from app.models import TODO
from django.contrib.auth.decorators import login_required

# ***************HOME**********************************


@login_required(login_url='login')
def home(request):
    if request.user.is_authenticated:
        user = request.user
        form = TODOForms()
        todos = TODO.objects.filter(user=user).order_by('priority')
        return render(request, 'index.html', context={'form': form, 'todos': todos})
    #  else:
    #     return redirect(login)

# **************SIGNUP***********************************


def signup(request):
    if request.method == "GET":
        form = UserCreationForm()
        context = {
            "form": form
        }
        return render(request, 'signup.html', context=context)
    else:
        print(request.POST)
        form = UserCreationForm(request.POST)
        context = {
            "form": form
        }
        if form.is_valid():
            user = form.save()
            print(user)
            if user is not None:
                return redirect('login')
        else:
            return render(request, 'signup.html', context=context)

# *****************LOGIN*******************************


def login(request):
    if request.method == "GET":
        form = AuthenticationForm()
        context = {
            'form': form
        }
        return render(request, 'login.html', context=context)
    else:
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                loginuser(request, user)
                return redirect('home')

        else:
            context = {
                'form': form
            }
            return render(request, 'login.html', context=context)

# ****************addtodo****************************


def addtodo(request):
    if request.user.is_authenticated:
        user = request.user
        form = TODOForms(request.POST)
        print(user)
        if form.is_valid():
            print(form.cleaned_data)
            todo = form.save(commit=False)
            todo.user = user
            todo.save()
            print(todo)
            return redirect("home")
        else:
            return render(request, 'index.html', context={'form': form})

#*****************signout**********************
def signout(request):
    logout(request)
    return redirect('login')

#********************delete-todo*****************

def deletetodo(request, id):
    TODO.objects.get(pk = id).delete()
    return redirect(home)
#********************changestatus*****************

def changestatus(request, id,status):
    todo= TODO.objects.get(pk = id)
    todo.status=status
    todo.save()
    return redirect(home)

