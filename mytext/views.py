from django.shortcuts import render
from mytext.models import Post,Borrow_book
from datetime import datetime
from django.shortcuts import redirect
from django.http import HttpResponse
from mytext.forms import UserRegisterForm,LoginForm

# Create your views here.
def homepage(request):
    posts = Post.objects.all()
    now = datetime.now()
    if request.user.is_authenticated:
        user_name = request.user.username
    else:
        user_name="未登入"
    return render(request ,'index.html', locals())

def showpost(request, slug):
    if request.user.is_authenticated:
        user_name = request.user.username
    else:
        user_name="未登入"
    post = Post.objects.get(slug=slug)
    try:
        if post != None:
            return render(request ,'post.html', locals())
        else:
            return redirect("/")
    except:
        return redirect("/")

def show_all_post(request):
    if request.user.is_authenticated:
        user_name = request.user.username
    else:
        user_name="未登入"
    post = Post.objects.all()
    return render(request, 'article_list.html', locals())

def show_comments(request, post_id):
    if request.user.is_authenticated:
        user_name = request.user.username
    else:
        user_name="未登入"
    #comments = Comment.objects.filter(post=post_id)
    comments = Post.objects.get(id=post_id).comment_set.all()
    return render(request, 'comments.html', locals())

from django.contrib.auth.models import User
#註冊
def register(request):
    if request.method == 'GET':
        form = UserRegisterForm()
        return render(request, 'register.html', locals())
    elif request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user_name = form.cleaned_data['user_name']
            user_email = form.cleaned_data['user_email']
            user_password = form.cleaned_data['user_password']
            user_password_confirm = form.cleaned_data['user_password_confirm']
            if user_password == user_password_confirm:
                user = User.objects.create_user(user_name, user_email, user_password)
                message = f'註冊成功！'
            else:
                message = f'兩次密碼不一致！'
        return redirect('/login')
    else:
        message = "ERROR"
        return render(request, 'register.html', locals())

from django.contrib.auth import authenticate,logout

#登入
def login(request):
    return render(request,'login.html',locals())

from django.contrib import auth
#使用者登入
def userLogin(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'userLogin.html', locals())
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user_name = form.cleaned_data['user_name']
            user_password = form.cleaned_data['user_password']
            user = authenticate(username=user_name, password=user_password)
            if user is not None:
                if user.is_active:
                    auth.login(request, user)
                    print("success")
                    message = '成功登入了'
                    return redirect('/')
                else:
                    message = '帳號尚未啟用'
            else:
                message = '登入失敗'
        return render(request, 'userLogin.html', locals())
    else:
        message = "ERROR"
        return render(request, 'userLogin.html', locals())
#圖書管理員登入
def managerLogin(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'managerLogin.html', locals())
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user_name = form.cleaned_data['user_name']
            user_password = form.cleaned_data['user_password']
            user = authenticate(username=user_name, password=user_password)
            if user is not None:
                if user.is_active:
                    auth.login(request, user)
                    print("success")
                    message = '成功登入了'
                    return redirect('/')
                else:
                    message = '帳號尚未啟用'
            else:
                message = '登入失敗'
        return render(request, 'managerLogin.html', locals())
    else:
        message = "ERROR"
        return render(request, 'managerLogin.html', locals())
#登出
def logouts(request):
    logout(request)

    return redirect('/')

def identity(user):
    if user.is_superuser:
        return "系統管理者"
    elif user.is_staff:
        return "圖書管理員"
    else:
        return "使用者"

#搜尋
from mytext.filter import BookFilter
def index(request):
    if request.user.is_authenticated:
        user_name = request.user.username
    else:
        user_name="未登入"
    books = Post.objects.all()
    bookFilter = BookFilter(queryset=books)
    if request.method == "POST":
        bookFilter = BookFilter(request.POST, queryset=books)
    context = {
        'bookFilter': bookFilter
    }
    return render(request, 'search.html', locals())

#Books 狀態
def condition(request, id):
    if request.use.is_active:
        c = Post.objects.get(id=id)





from django.utils import timezone
# 借書
def borrow_book(request,book_id):
    if request.user.is_active:
        book = Post.objects.get(id=book_id)
        quantity = int(book.quantity)
        if quantity > 0:
            due_date = timezone.now() + timezone.timedelta(days=40)
            borrow_books = Borrow_book.objects.create(
                readerID = request.user,
                title = book,
                borrow_date = timezone.now(),
                due_date = due_date,
                returned = False,
            )
            book.quantity -= 1
            book.save()
            return render(request, 'borrow.html', {'borrow_book':borrow_books,'message': "借閱成功"})
        else:
            message = "此書暫不可借"
            return render(request, 'borrow.html',locals())
    else:
        return render(request, 'login.html', locals())

from django.contrib.auth.decorators import login_required

@login_required
def getBorrowListByUser(request):
    if request.user.is_authenticated:
        user_name = request.user.username
    else:
        user_name="未登入"
    current_user = request.user
    borrowList = Borrow_book.objects.filter(readerID=current_user).order_by('-borrow_date', '-returned')
    identityName = identity(current_user)
    return render(request, 'borrowbook.html', locals())
