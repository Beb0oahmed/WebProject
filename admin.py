# admin.py
from django.contrib import admin
from .models import Book
from .models import sign


class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'category', 'status')
    list_editable = ('status',)  # Allow status to be editable in the list view
   

admin.site.register(Book, BookAdmin)
admin.site.register(sign)
