from django.db import models 

from django.contrib.auth.models import User

class Post(models.Model):
    GENRE_CHOICES = (
        ('fairy tale', '童話'),
        ('comic', '漫畫'),
    )
    CONDITION_CHOICES = (
        ('loan','外借中'),
        ('collection','館藏中'),
        ('reserve','預約中')
    )
    title = models.CharField(max_length=200)
    slug = models.CharField(max_length=200)
    genre = models.CharField(max_length=200, choices=GENRE_CHOICES)
    author = models.CharField(max_length=50)
    condition = models.TextField()
    body = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.text
    
class Borrow_book(models.Model):  
    readerID = models.ForeignKey(User, on_delete=models.PROTECT)  
    title = models.ForeignKey(Post, on_delete=models.PROTECT)  
    borrow_date = models.DateTimeField()  #借書時間
    due_date = models.DateTimeField()     #到期日
    return_date = models.DateTimeField(blank=True, null=True)   #還書時間
    class Meta:
        unique_together = ("readerID", "title", "borrow_date")
