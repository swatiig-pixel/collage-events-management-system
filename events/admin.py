from django.contrib import admin
from .models import Category, Venue, Club, Event, ClubMember,EventRegistration

# Register your models here.

admin.site.register(Category)
admin.site.register(Venue)
admin.site.register(Club)
admin.site.register(Event)
admin.site.register(ClubMember)
admin.site.register(EventRegistration)