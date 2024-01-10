from django.shortcuts import render
from mytext.models import Post,Borrow_book
from datetime import datetime
from django.shortcuts import redirect
from django.http import HttpResponse
from mytext.forms import UserRegisterForm,LoginForm
from django.utils import timezone
from django.contrib import auth,messages
from django.contrib.auth import authenticate,logout
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password

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

#登入
def login(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', locals())
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
        return render(request, 'login.html', locals())
    else:
        message = "ERROR"
    return render(request,'login.html',locals())

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
def borrow_book(request,post_id):
    if request.user.is_active:

        book = Post.objects.get(id=post_id)
        if Borrow_book.objects.filter(readerID=request.user, returned=False, title=book) :
            message = "此書以借閱，請歸還後再借閱!"
            text='重複借閱'
            return render(request, 'borrow.html',locals())
        elif book.quantity==0:
            message = "此書暫不可借，請先借閱別本書!"
            text='館藏已無'
            return render(request, 'borrow.html',locals())
        else:   
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
                return render(request, 'borrow.html', {'borrow_book':borrow_books,'message':"借閱成功", 'text':"借書"})
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

#還書
def returnBook(request, return_id):
    if request.user =='POST':
        returnBook=request.POST.getlist('return_books')
        returnCorrect = []
        u = None
        for record in returnBook:
            record = Borrow_book.objects.get(id=record)
            record.is_returned=True
            record.actual_return_date=timezone.now()
            returnCorrect.append(record)
            record.save()
            record.book.available_quantity += 1
            record.book.save()
            u=record.user
        return render(request, 'returnBook.html',{'returnCorrect':returnCorrect,'u':u})
    else:
        return redirect('/')

def returnBookPage(request):
    if request.method=='POST':
        name=request.POST.get('username')
        if User.objects.filter(username=name).exists():
            user=User.objects.get(username=request.POST.get('username'))
            returnList=Borrow_book .objects.filter(user=user, is_returned=False).order_by('due_date')
            return render(request,'returnBookPage.html',locals())
        else:
            return render(request,'returnBookPage.html',{'msg':'查無此用戶'})

    else:
        return render(request,'returnBookPage.html',{'msg':' '})

#修改密碼
def changePassword(request):
    if request.method=='POST':
        password=request.POST.get('password')
        newPassword1=request.POST.get('newPassword1')
        newPassword2=request.POST.get('newPassword2')
        if not check_password(password, request.user.password):
            return render(request, 'changePassword.html', {'msg':'原密碼輸入錯誤'})
        elif newPassword1 != newPassword2:
            return render(request, 'changePassword.html', {'msg':'兩次密碼不一致！'})
        else:
            request.user.set_password(newPassword1)
            request.user.save()
            messages.success(request, '密碼修改成功，請重新登入')
            return redirect('login')
    return render(request, 'changePassword.html')

#新增書籍
def addBook(request):
    GENRE_CHOICES = ('請選擇','童話','漫畫')
    if request.method=='POST':
        title=request.POST.get('title')
        slug=request.POST.get('slug')
        genre=request.POST.get('genre')
        author=request.POST.get('author')
        quantity=request.POST.get('quantity')
        body=request.POST.get('body')
        Post.objects.create(
            title=title,
            slug=slug,
            genre=genre,
            author=author,
            quantity=quantity,
            body=body)
        message='書籍新增成功'
        text='書籍新增'
        return render(request, 'borrow.html', locals())
    else:
        return render(request, 'addBook.html', locals())

def bookManagePage(request):
    if request.user.is_staff:
        PostList=Post.objects.all()
        return render(request, 'bookManagePage.html',locals())
    else:
        return redirect('/')

def bookModify(request, post_id):
    if Post.objects.filter(id=post_id).exists():
        post=Post.objects.get(id=post_id)
        if request.method=='POST':
            title=request.POST.get('title')
            slug=request.POST.get('slug')
            genre=request.POST.get('genre')
            author=request.POST.get('author')
            quantity=request.POST.get('quantity')
            body=request.POST.get('body')

            post.title=title
            post.slug=slug
            post.genre=genre
            post.author=author
            post.quantity=quantity
            post.body=body

            post.save()
            message='書籍修改成功'
            text='書籍修改'
            return render(request, 'borrow.html', locals())
        else:
            return render(request, 'bookModify.html',locals())
    else:
        return redirect('/')

def returnBookPage(request):
    if request.method=='POST':
        name=request.POST.get('username')
        if User.objects.filter(username=name).exists():
            user=User.objects.get(username=request.POST.get('username'))
            returnList=borrow_book.objects.filter(user=user, is_returned=False).order_by('due_date')
            return render(request,'returnBookPage.html',locals())
        else:
            return render(request,'returnBookPage.html',{'msg':'查無此用戶'})

    else:
        return render(request,'returnBookPage.html',{'msg':' '})

def returnBook(request):
    if request.method=='POST':
        u=None
        returnCorrect=[]
        returnBookList=request.POST.getlist('return_books')
        for recordingId in returnBookList:
            recording=borrow_book.objects.get(id=recordingId)
            recording.returned=True
            recording.actual_return_date=timezone.now()
            returnCorrect.append(recording)
            recording.save()

            recording.book.quantity += 1
            recording.book.save()
            u=recording.user
        return render(request, 'returnBook.html',{'returnCorrect':returnCorrect,'u':u})
    else:
        return redirect('/returnBookPage/')

def postPage(request, slug):
    post=Post.objects.filter(slug=slug)
    if post:
        post=post.first()
        return render(request, 'postPage.html', locals())
    else:
        return redirect('/')