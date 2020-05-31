from django.shortcuts import render, redirect
from .models import User, UserManager, Book, Author, Review
import bcrypt
from django.contrib import messages
from time import strftime, gmtime


def index(request):
    all_users = User.objects.all()
    request.session['log_email'] = []
    book = Book.objects.get(id=11)
    print(book.authors.all())
    return render(request, "index.html")


def registration(request):
    errors = User.objects.user_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        if request.method == "POST":
            name = request.POST['name']
            alias = request.POST['alias']
            email = request.POST['email']
            pw = request.POST['password']
            confirm_pw = request.POST['confirm_pw']
            pw_hash = bcrypt.hashpw(pw.encode(), bcrypt.gensalt()).decode()
            # confirm password stuff here
            if bcrypt.checkpw(confirm_pw.encode(), pw_hash.encode()) == True:
                User.objects.create(fullname=name, alias=alias,
                                    email=email, password=pw_hash)
                request.session['log_email'] = email
                request.session['log_password'] = pw_hash
                request.session['log_name'] = name
                request.session['log_alias'] = alias
            else:
                errors['pwconfirm'] = "Lol pw didnt match, noob"
                if len(errors) > 0:
                    for key, value in errors.items():
                        messages.error(request, value)
                    return redirect('/')
    return redirect("/books")


def log_in(request):
    if request.method == "POST":
        log_email = request.POST['log_email']
        log_pw = request.POST['log_pw']
        if User.objects.filter(email=log_email):
            request.session['log_email'] = log_email
            request.session['log_pw'] = log_pw
            return redirect("/books")


def success_log_in(request):
    # if 'message' not in request.session:
    #     request.session['message'] = []
    logged_user = User.objects.filter(email=request.session['log_email'])
    # print(logged_user)
    # print(logged_user[0].id)
    logged_user_name = logged_user[0].fullname
    logged_user_alias = logged_user[0].alias
    user_id = logged_user[0].id
    # messages = Message.objects.all()
    # comments = Comment.objects.all()
    request.session['id'] = user_id
    all_reviews = Review.objects.all()
    all_books = Book.objects.all()
    context = {
        "name": logged_user_name,
        # "session_messages": request.session['message'],
        "time": strftime("%m-%d-%y"),
        "user_id": user_id,
        # "messages": messages,
        # "comments": comments,
        "session_id": request.session['id'],
        "reviews": all_reviews,
        "books": all_books,
    }
    return render(request, "books.html", context)


def add_book_page(request):
    all_authors = Author.objects.all()
    context = {
        "authors": all_authors,
    }
    return render(request, "addbookpage.html", context)


def add_book(request):
    if request.method == "POST":
        title = request.POST['title']
        addauthor = request.POST['addauthor']
        review = request.POST['review']
        rating = int(request.POST['rating'])
        user = User.objects.filter(email=request.session['log_email'])
        user_id = user[0].id
        adduser = User.objects.get(id=user_id)
        new_book = Book.objects.create(title=title)
        if addauthor != "":
            new_author = Author.objects.create(fullname=addauthor)
            new_author.books.add(new_book)
        else:
            author = request.POST['authorselect']
            new_author = Author.objects.create(fullname=author)
            new_author.books.add(new_book)
        new_review = Review.objects.create(
            user=adduser, book=new_book, content=review, rating=rating)

    return redirect('/books')


def book_page(request, book_id):
    book = Book.objects.get(id=book_id)
    authors = book.authors.all()
    author = authors[0].fullname
    context = {
        "book": book,
        "author": author,
    }
    return render(request, "bookpage.html", context)


def add_review(request):
    user = User.objects.filter(email=request.session['log_email'])
    user_id = user[0].id
    adduser = User.objects.get(id=user_id)
    content = request.POST['addreview']
    rating = request.POST['addrating']
    book_id = request.POST['book_id']
    book = Book.objects.get(id=book_id)
    new_review = Review.objects.create(
        user=adduser, book=book, content=content, rating=rating)
    return redirect(f'/books/{book_id}')


def delete_review(request, review_id):
    review = Review.objects.get(id=review_id)
    book = review.book.title
    book_id = review.book.id
    review.delete()
    return redirect(f'/books/{book_id}')


def user_page(request, user_id):
    user = User.objects.get(id=user_id)
    alias = user.alias
    name = user.fullname
    email = user.email
    count = 0
    for review in user.reviews.all():
        count += 1
    context = {
        "alias": alias,
        "name": name,
        "email": email,
        "reviews": count,
        "total_reviews": user.reviews.all(),
    }
    return render(request, "userpage.html", context)


def log_out(request):
    request.session['log_email'] = []
    request.session['log_pw'] = []
    return redirect('/')
