from django.contrib import admin
from mytext.models import Post, Comment, Borrow_book

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug','genre','author', 'condition','quantity','pub_date')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('text','pub_date', 'post')

class Borrow_booksAdmin(admin.ModelAdmin):
    list_display = ('readerID','title','borrow_date','due_date',"returned")
admin.site.register(Borrow_book, Borrow_booksAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
