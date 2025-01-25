from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from rest_framework import viewsets, status
from django.utils.timezone import now
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import EventSerializer
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from events.forms import EventForm, CommentForm
import requests

#Zobrazuje přihlášení
def login_view(request):
    if request.method == 'POST':
        username = request.POST['Přihlašovací jméno']
        password = request.POST['Heslo']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('event_list')
    return render(request, 'events/login.html')

#Možnost odhlášení
def user_logout(request):
    logout(request)
    return redirect(request.META.get('HTTP_REFERER', '/'))

#Zobrazuje odhlášení
def logout_view(request):
    logout(request)
    return redirect('event_list')

#Zobrazuje registraci událostí
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'events/register.html', {'form': form})

#Importy hlavní stránky
from django.shortcuts import render
from .models import Event, Comment, Promotion

#Zobrazuje hlavní stránku
def home(request):
    events = Event.objects.all()
    comments = Comment.objects.all()
    promotions = Promotion.objects.all()
    print(promotions)
    return render(request, 'home.html', {'events': events, 'comments': comments, 'promotions': promotions})

#Zobrazuje přidávání nových událostí
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

#Zobrazuje seznam událostí
def event_list(request):
    events = Event.objects.all()
    return render(request, "events/event_list.html", {"events": events})

#Zobrazuje detail události
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

    return render(request, 'events/event_detail.html', {'event': event, 'comments': comments, 'form': form})

#Zobrazuje vyhledávač událostí
def search_results(request):
    query = request.GET.get('query', '')
    filter_option = request.GET.get('filter', 'all')

    events = Event.objects.all()

    if query:
        events = events.filter(title__icontains=query)

    if filter_option == 'future':
        # Nastávající akce: které ještě nezačaly
        events = events.filter(start_date__gt=now())
    elif filter_option == 'ongoing_future':
        # Probíhající akce: které už začaly, ale ještě neskončily
        events = events.filter(start_date__lte=now(), end_date__gte=now())
    elif filter_option == 'past':
        events = events.filter(end_date__lt=now())

    return render(request, 'events/search_results.html', {'events': events, 'query': query, 'filter_option': filter_option})

#Zobrazení stránky o nás
def about(request):
    return render(request, 'about.html')

#
class EventViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    # snadný přístup do API http://127.0.0.1:8000/api/events/upcoming/
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

#Zobrazení přidávání události
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

#Jenom admin může upravovat událost
@login_required
def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.user != event.created_by and not request.user.is_staff:
        return HttpResponseForbidden("Nemáte oprávnění na úpravu události.")

    if request.method == "POST":
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event_detail', event_id=event.id)
    else:
        form = EventForm(instance=event)

    return render(request, 'events/edit_event.html', {'form': form, 'event': event})

#API pro vyhladávání událostí z jiných webů - ze stránky kudy z nudy nám na API neudelii přístup
API_URL = "https://www.kudyznudy.cz/kalendar-akci/api-events/"

def api_event_list(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    params = {}
    if start_date:
        params['start_date'] = start_date
    if end_date:
        params['end_date'] = end_date

    print(f"Fetching events with params: {params}")  # Debug na vyhledávání

    try:
        response = requests.get(API_URL, params=params)
        response.raise_for_status()
        print(f"API Response: {response.text}")  # Debug log
        events = response.json()
    except requests.RequestException as e:
        print(f"Error fetching events: {e}")
        events = []

    return render(request, 'events/api_event_list.html', {'events': events})
