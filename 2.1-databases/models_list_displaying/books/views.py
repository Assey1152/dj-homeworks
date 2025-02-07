from datetime import datetime

from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect

from books.models import Book


def index(request):
    return redirect('books')


def books_view(request):
    template = 'books/books_list.html'
    books = Book.objects.all()
    context = {
        'books': books,
    }
    return render(request, template, context)


def books_to_date(request, dt: datetime):
    books = Book.objects.all()
    pub_dates = sorted([b.pub_date.strftime('%Y-%m-%d') for b in books])
    search_date = dt.strftime('%Y-%m-%d')
    if search_date in pub_dates:
        filtered_books = [book for book in books if book.pub_date == dt.date()]
        paginator = Paginator(pub_dates, 1)
        page = paginator.get_page(pub_dates.index(search_date) + 1)
        next_page = ''
        prev_page = ''
        if page.has_next():
            next_page = pub_dates[page.next_page_number() - 1]
        if page.has_previous():
            prev_page = pub_dates[page.previous_page_number() - 1]
        context = {
            'books': filtered_books,
            'page': page,
            'next_page': next_page,
            'prev_page': prev_page,
        }
        return render(request, 'books/books_list.html', context)
    else:
        return HttpResponse('В библиотеке нет книг, опубликованных в эту дату')
