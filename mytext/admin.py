from django.contrib import admin
from mytext.models import Post, Comment
# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'pub_date')
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)


