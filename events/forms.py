from django import forms
from django.utils import timezone
from .models import Event, Comment

# Přidávání nových událostí
class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'start_date', 'end_date', 'description', 'location']
        labels = {
            'title': 'Název',
            'start_date': 'Datum začátku',
            'end_date': 'Datum konce',
            'description': 'Popis',
            'location': 'Místo',
        }
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    # Předchází chybám v názvu události
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title or title.strip() == "":
            raise forms.ValidationError("Nadpis nemůže být prázdný nebo obsahovat pouze mezery.")
        return title

    # Určuje minimální počet znaků v popisku události
    def clean_description(self):
        description = self.cleaned_data.get('description')
        if len(description) < 20:
            raise forms.ValidationError("Popis musí obsahovat minimálně 20 znaků.")
        return description

    # Datum od nemůže být v minulosti
    def clean_start_date(self):
        start_date = self.cleaned_data.get('start_date')
        if start_date and start_date < timezone.now():
            raise forms.ValidationError('Datum od nemůže být v minulosti.')
        return start_date

    # Datum od nemůže být později než datum do
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date and start_date > end_date:
            raise forms.ValidationError("Datum od nemůže být později než datum do.")
        return cleaned_data

# Přidávání komentáře v editu
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

# Formulář pro přihlášení na událost
class AttendEventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['attendees']

# Formulář pro odhlášení z události
class UnattendEventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = []
