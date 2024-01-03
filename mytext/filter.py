from .models import Post
import django_filters
from django import forms

class BookFilter(django_filters.FilterSet):

    title = django_filters.CharFilter(
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'class': 'form-control'}))
 
    genre = django_filters.CharFilter(
        widget=forms.Select(choices=(('', '請選擇'),) + Post.GENRE_CHOICES, attrs={'class': 'form-control'}))
 
    author = django_filters.CharFilter(
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    
    class Meta:
        model = Post
        fields = '__all__'