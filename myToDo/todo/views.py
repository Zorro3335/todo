from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import InternalError
from django.contrib.auth import login, logout, authenticate
from .forms import ToDoForms
from .models import ToDo
from django.utils import timezone


# Create your views here.


def home(request):
    return render(request, 'todo/home.html')


def singupuser(request):
    if request.method == 'GET':
        return render(request, 'todo/singupuser.html', {'form_user': UserCreationForm})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'],
                                                password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('current_todos')
            except InternalError as e:
                return render(request, 'todo/singupuser.html',
                              {'form_user': UserCreationForm, 'error': 'Это имя пользователя уже используется.'})
        else:
            return render(request, 'todo/singupuser.html',
                          {'form_user': UserCreationForm, 'error': 'Пароль не совпадает.'})


def login_user(request):
    if request.method == 'GET':
        return render(request, 'todo/login_user.html', {'form_user': AuthenticationForm})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todo/login_user.html', {'form_user': AuthenticationForm,
                                                            'error': 'Такого пользователя нет'})
        login(request, user)
        return redirect('home')


def create_todo(request):
    if request.method == 'GET':
        return render(request, 'todo/create_todo.html', {'form_user': ToDoForms})
    else:
        form = ToDoForms(request.POST)
        new_todo = form.save(commit=False)
        new_todo.user = request.user
        new_todo.save()
        return redirect('current_todos')


def current_todos(request):
    print(request)
    data = ToDo.objects.filter(user=request.user, deadline__isnull=True).order_by('-create_date')
    return render(request, 'todo/current_todos.html',
                  {'datas': data if data else 'На даннный момент у Вас нет активных задач. Хотите создать?'})


def view_completed_todo(request):
    data = ToDo.objects.filter(user=request.user, deadline__isnull=False).order_by('-deadline')
    return render(request, 'todo/completed_todo.html', {'datas': data if data else
    'На даннный момент у Вас нет выполненных задач.'})


def completed_todo(request, id_todo):
    todo = get_object_or_404(ToDo, pk=id_todo, user=request.user)
    todo.deadline = timezone.now()
    todo.save()
    print(todo)
    return redirect('current_todos')


def delete_todo(request, id_todo):
    todo = get_object_or_404(ToDo, pk=id_todo, user=request.user)
    todo.delete()
    return redirect('current_todos')


def save_todo(request, id_todo):
    todo = get_object_or_404(ToDo, pk=id_todo, user=request.user)
    todo.save()
    return redirect('current_todos')


def detail_todo(request, id_todo):
    todo = get_object_or_404(ToDo, pk=id_todo, user=request.user)
    if request.method == 'GET':
        form = ToDoForms(instance=todo)
        return render(request, 'todo/detail_todo.html', {'todo': todo, 'detail_todo': form})
    else:
        try:
            form = ToDoForms(request.POST or None, instance=todo)
            form.save()

            return redirect('current_todos')
        except ValueError:
            return render(request, 'todo/detail_todo.html',
                          {'todo': todo, 'detail_todo': todo, 'error': 'Не те данные'})


def logout_user(request):
    if request.method == 'GET':
        logout(request)
        return redirect('home')


