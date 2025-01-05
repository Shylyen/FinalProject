from django import forms
from .models import Event
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'start_date', 'location']

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=100)
    name = forms.CharField(max_length=50)

    class Meta:
        model = CustomUser
        fields = ['email', 'name', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered.")
        return email

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name.strip():
            raise ValidationError("Name cannot be empty or contain only spaces.")
        return name

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if len(password) < 8 or len(password) > 30:
            raise ValidationError("Password must be between 8 and 30 characters.")
        return password