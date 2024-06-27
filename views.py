from django.shortcuts import render,get_object_or_404, redirect
from .models import Book
from .models import sign
from .forms import BookForm
from django.db.models import Q
from django.http import JsonResponse
from .forms import signform
from .forms import LoginForm
from django.urls import reverse
from django.contrib.auth.hashers import make_password, check_password

#from django.http import HttpResponse
# Create your views here. controles what appears and what not

def about(request):
     return render(request,'pages/about.html')

def borrowed(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        borrowed_books = Book.objects.filter(status=False)
        results = [
            {
                'title': book.title,
                'author': book.author,
                'category': book.category,
                'cover_photo': book.cover_photo.url if book.cover_photo else '',
                'id': book.id
            } for book in borrowed_books
        ]
        return JsonResponse({'books': results})
            
    else:
        return render(request,'pages/borrowed.html')
        
    

def signup(request):
    if request.method == "POST":
        x = request.POST.get('username')  # value of user
        z = request.POST.get('last')
        l = request.POST.get('email')
        v = request.POST.get('pass')
        c = request.POST.get('con')
        admin = request.POST.get('is_admin') == 'on'
        user = request.POST.get('is_user') == 'on'

        # Validation checks
        if not x or not z or not l or not v or not c:
            return render(request, 'pages/signup.html', {'lf': LoginForm, 'error': 'All fields must be filled out'})

        if len(v) < 8:
            return render(request, 'pages/signup.html', {'lf': LoginForm, 'error': 'Password must be at least 8 characters long'})

        if v != c:
            return render(request, 'pages/signup.html', {'lf': LoginForm, 'error': 'Passwords do not match'})

        data = sign(username=x, password=v, last=z, email=l,user=user , admin=admin)  # data will show here
        data.save()
        return render(request, 'pages/signup.html', {'lf': signform, 'success': 'Registered Successfully!'})

    return render(request, 'pages/signup.html', {'lf': signform})
     

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('pass')
        user = sign.objects.get(email=email)
        if user is not None:
            if password == user.password:
                if user.admin:
                    return redirect('homeadmin')
                else:
                    return redirect('homeuser')
            else:
                return render(request, '../templates/pages/login.html', {'error': 'Invalid credentials'})
        else:
            return render(request, '../templates/pages/login.html', {'error': 'Invalid credentials'})
    return render(request, '../templates/pages/login.html')


def homeuser(request):
    query = request.GET.get('query', '')
    books = Book.objects.all()
    if query:
        books = books.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(category__icontains=query)
        )
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        results = [
            {
                'title': book.title,
                'author': book.author,
                'category': book.category,
                'cover_photo': book.cover_photo.url if book.cover_photo else '',
                'url': reverse('bookpguser', args=[book.id])
            } for book in books
        ]
        return JsonResponse(results, safe=False)

    return render(request, 'pages/homeuser.html', {'books': books, 'query': query})

def homeadmin(request):
    books = Book.objects.all()  
    return render(request, 'pages/homeadmin.html', {'books': books})



def addbook(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('homeadmin')  # Redirect after POST to avoid resubmitting the form
    else:
        form = BookForm()
    return render(request, 'pages/addbook.html', {'form': form})


def home(request):
    query = request.GET.get('query', '')
    books = Book.objects.filter(status=True)
    if query:
        books = books.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(category__icontains=query)
        )

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        results = [
            {
                'title': book.title,
                'author': book.author,
                'category': book.category,
                'cover_photo': book.cover_photo.url if book.cover_photo else ''
            } for book in books
        ]
        return JsonResponse(results, safe=False)

    return render(request, 'pages/home.html', {'books': books, 'query': query})


def edit(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect('homeadmin')  # Replace with your book detail view
    else:
        form = BookForm(instance=book)
    return render(request, 'pages/edit.html', {'form': form, 'book': book})

def delete_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    book.delete()
    return redirect('homeadmin')

def bookpg(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    return render(request, 'pages/bookpg.html', {'book': book})

def bookpguser(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    return render(request, 'pages/bookpguser.html', {'book': book})

def borrow_book(request,book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.method == "POST":
        if book.status == True:
            book.status = False
            book.save()
            return redirect('borrowed')
            
    return render(request, 'bookpguser.html', {'book': book})
    