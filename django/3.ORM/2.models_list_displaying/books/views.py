from django.shortcuts import redirect, render
from .models import Book


def index_view(request):
    return redirect('books')


def books_view(request):
    template = 'books/books_list.html'
    books = Book.objects.all()
    context = {'books': books}
    return render(request, template, context)


def books_date_view(request, date):
    template = 'books/books_list_pagi.html'
    format = '%Y-%m-%d'
    books = Book.objects.filter(pub_date=date)

    previous_page = Book.objects.filter(pub_date__lt=date).values('pub_date').first()
    if previous_page:
        previous_page = previous_page.get('pub_date').strftime(format)
    next_page = Book.objects.filter(pub_date__gt=date).values('pub_date').first()
    if next_page:
        next_page = next_page.get('pub_date').strftime(format)

    context = {'books': books,
               'previous_page': previous_page,
               'next_page': next_page}
    return render(request, template, context)
