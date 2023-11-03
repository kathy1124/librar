from django.shortcuts import render
from mytext.models import Post
from datetime import datetime
from django.shortcuts import redirect

# Create your views here.
def homepage(request):
    posts = Post.objects.all()
    now = datetime.now()
    return render(request ,'index.html', locals())

def showpost(request, slug):
    post = Post.objects.get(slug=slug)
    try:
        if post != None:
            return render(request ,'post.html', locals())
        else:
            return redirect("/")
    except:
        return redirect("/")
    
def login(request):
    return render(request, 'login.html')

def books(request):
    return render(request, 'books.html')