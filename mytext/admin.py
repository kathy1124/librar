from django.contrib import admin
from mytext.models import Post, Comment

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug','genre','author', 'pub_date')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('text','pub_date', 'post')
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
