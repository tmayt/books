from django.contrib import admin
from .models import Book, Bookmark, Comment

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date')
    search_fields = ('title', 'author')
    list_filter = ('published_date',)
    ordering = ('title',)

class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'added_on')
    search_fields = ('user__username', 'book__title')
    list_filter = ('added_on',)
    ordering = ('-added_on',)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'rating', 'submitted_on')
    search_fields = ('user__username', 'book__title')
    list_filter = ('rating', 'submitted_on')
    ordering = ('-submitted_on',)

admin.site.register(Book, BookAdmin)
admin.site.register(Bookmark, BookmarkAdmin)
admin.site.register(Comment, CommentAdmin)
