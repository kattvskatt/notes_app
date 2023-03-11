from django.contrib import admin

from .models import *

class NotesAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'time_create', 'time_update', 'image', 'category')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    # list_editable = ('category',)
    list_filter = ('category', 'time_create', 'time_update')
    prepopulated_fields = {'slug': ('title',)}

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Notes, NotesAdmin)
admin.site.register(Category, CategoryAdmin)