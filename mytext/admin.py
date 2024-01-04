from django.contrib import admin
from mytext.models import Post, Comment, Borrow_book

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug','genre','author', 'condition','pub_date')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('text','pub_date', 'post')

class Borrow_booksAdmin(admin.ModelAdmin):
    list_display = ('readerID','title','borrow_date','due_date',"return_date")
    
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Borrow_book, Borrow_booksAdmin)