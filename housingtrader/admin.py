# -*- coding: utf-8 -*- 
from housingtrader.models import Listing, get_listing_fields_by_prefix
from django.contrib import admin


class ListingAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Användare', {'fields':['user']}),
        ('Finnes', {'fields':get_listing_fields_by_prefix('o_')}),
        ('Sökes', {'fields':get_listing_fields_by_prefix('w_')})
    ]
    raw_id_fields = ('user',)
    
admin.site.register(Listing, ListingAdmin)