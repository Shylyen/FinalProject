from django.contrib import admin
from .models import Event, Registration, Comment, Promotion

# Tabulky v adminech, tabulky na úpravy
admin.site.register(Event)
admin.site.register(Comment)
admin.site.register(Registration)
admin.site.register(Promotion)
