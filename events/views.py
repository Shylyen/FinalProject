from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .models import Event
from .forms import EventForm
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm

# Login View
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            form = AuthenticationForm()
        return render(request, 'events/login.html')

# Logout View
def logout_view(request):
    logout(request)
    return redirect('home')

# Register View
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'events/register.html', {'form': form})

# Home Page View
def home(request):
    events = Event.objects.all()
    return render(request, 'home.html', {'events': events})

# Add Event View (Requires Login)
@login_required
def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.creator = request.user  # Set the creator to the current user
            event.save()
            return redirect('event_list')  # Redirect to event list or event details page
    else:
        form = EventForm()
    return render(request, 'events/add_event.html', {'form': form})

# Event List View
def event_list(request):
    events = Event.objects.all()
    return render(request, 'events/event_list.html', {'events': events})

# Event Detail View
def event_detail(request, event_id):
    event = Event.objects.get(id=event_id)
    return render(request, 'events/event_detail.html', {'event': event})