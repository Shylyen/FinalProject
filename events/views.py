# events/views.py

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

from events.forms import EventForm
from events.models import Event


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('event_list')
    return render(request, 'events/login.html')

def logout_view(request):
    logout(request)
    return redirect('event_list')

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'events/register.html', {'form': form})

def home(request):
    return render(request, "home.html")


def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user
            event.save()
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'add_event.html', {'form': form})

def event_list(request):
    events = Event.objects.all()
    return render(request,"events/event_list.html",{"events":events})