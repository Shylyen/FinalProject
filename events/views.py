# events/views.py
from datetime import timezone
from turtledemo.clock import datum
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from events.forms import EventForm
from django.shortcuts import render, get_object_or_404, redirect
from .models import Event
from .forms import CommentForm
from rest_framework import viewsets, status
from django.utils.timezone import now
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets
from .models import Event
from .serializers import EventSerializer
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseForbidden
from events.forms import EventForm, CommentForm
from events.models import Event
import requests


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
    return render(request, 'events/add_event.html', {'form': form})

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

def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    comments = event.comments.all()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.event = event
            comment.user = request.user
            comment.save()
            return redirect('event_detail', event_id=event.id)
    else:
        form = CommentForm()

    return render(request, 'events/event.detail.html', {'event': event, 'comments': comments, 'form': form})

def about(request):
    return render(request, 'about.html')


class EventViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


    # snadný přístup dp API http://127.0.0.1:8000/api/events/upcoming/

    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        start_time = request.query_params.get('start_date', None)
        end_time = request.query_params.get('end_date', None)
        events = Event.objects.filter(start_date__gte=now())

        if start_time:
            events = events.filter(start_date__gte=start_time)
        if end_time:
            events = events.filter(end_date__lte=end_time)

        serializer = self.get_serializer(events, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def detail(self, request, pk=None):
        event = get_object_or_404(Event, pk=pk)
        serializer = self.get_serializer(event)
        return Response(serializer.data)


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    @action(detail=False, methods=['post'])
    def create_event(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)







def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    comments = event.comments.all()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.event = event
            comment.user = request.user
            comment.save()
            return redirect('event_detail', event_id=event.id)
    else:
        form = CommentForm()

    return render(request, 'events/event.detail.html', {'event': event, 'comments': comments, 'form': form})


@login_required
def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    # Only allow the creator or an admin to edit
    if request.user != event.created_by and not request.user.is_staff:
        return HttpResponseForbidden("You do not have permission to edit this event.")

    if request.method == "POST":
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event_detail', event_id=event.id)
    else:
        form = EventForm(instance=event)

    return render(request, 'events/edit_event.html', {'form': form, 'event': event})


API_URL = "https://www.kudyznudy.cz/kalendar-akci/api-events/"

def api_event_list(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    params = {}
    if start_date:
        params['start_date'] = start_date
    if end_date:
        params['end_date'] = end_date

    print(f"Fetching events with params: {params}")  # Debug log

    try:
        response = requests.get(API_URL, params=params)
        response.raise_for_status()
        print(f"API Response: {response.text}")  # Debug log
        events = response.json()
    except requests.RequestException as e:
        print(f"Error fetching events: {e}")
        events = []

    return render(request, 'events/api_event_list.html', {'events': events})

