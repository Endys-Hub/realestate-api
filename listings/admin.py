from django.contrib import admin
from .models import Listing, Enquiry

admin.site.register(Listing)
admin.site.register(Enquiry)

'''
@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'is_published', 'is_available')
    list_editable = ('is_published', 'is_available')

@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'listing', 'created_at')
'''