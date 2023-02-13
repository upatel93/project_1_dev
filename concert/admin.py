from django.contrib import admin
from .models import Concert, ConcertTicket

class ConcertInline(admin.TabularInline):
    model = ConcertTicket

@admin.register(Concert)
class ConcertAdmin(admin.ModelAdmin):
    inlines = [
        ConcertInline
    ]
    list_display = ['name', 'available_seats', 'total_seats', 'date', 'time']
