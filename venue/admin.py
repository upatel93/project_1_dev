from django.contrib import admin
from .models import Venue, SeatType
# Register your models here.


class VenueSeatInline(admin.TabularInline):
    model = SeatType
    min_num = 1
    max_num = 10

@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    inlines = [
        VenueSeatInline
    ]
    list_display = ['name', 'location', 'total_seats']