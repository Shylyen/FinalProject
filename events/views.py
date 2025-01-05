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

def user_logout(request):
    logout(request)
    return redirect(request.META.get('HTTP_REFERER', '/'))

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

def event_detail(request,pk):
    event= Event.objects.get(id=pk)
    return render(request, "events/event.detail.html", {"event": event})

def search_results(request):
    query = request.GET.get('query', '')
    filter_option = request.GET.get('filter', 'all')

    events = Event.objects.all()

    if query:
        events = events.filter(title__icontains=query)

    if filter_option == 'future':
        events = events.filter(start_date__gte=timezone.now())
    elif filter_option == 'ongoing_future':
        events = events.filter(end_date__gte=timezone.now())

    return render(request, 'events/search_results.html', {'events': events, 'query': query, 'filter_option': filter_option})