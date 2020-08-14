from django.contrib import admin
from .models import Attraction,Review


class AttractionAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'info')


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'date', 'author', 'attraction', 'rating')


admin.site.register(Attraction, AttractionAdmin)
admin.site.register(Review, ReviewAdmin)
