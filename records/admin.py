from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(Visitor)
class VisitorAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'surname', 'organization', 'position', 'country_of_origin', 'id_passport_nbr', 'email', 'address', 'mobile_phone']

@admin.register(Movement)
class MovementAdmin(admin.ModelAdmin):
    list_display = ['purpose','devices', 'time_in', 'time_out', 'devices', 'comment', 'card']


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ['name', 'number']


@admin.register(WaitingList)
class WaitingListAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'surname', 'organization', 'position', 'country_of_origin', 'id_passport_nbr', 'email', 'address', 'mobile_phone']
