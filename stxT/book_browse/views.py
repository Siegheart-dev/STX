from django.shortcuts import render, redirect
import requests
import environ
from .forms import BookSearch
from .models import *
from django.db.models import Q

env = environ.Env()
env.read_env()
key = env.str('API_KEY')

def index(request):
    form = BookSearch()
    return render(request, 'book_browse/index.html', {'form': form})


def books(request):

    author = request.GET.get('author', False)
    search = author if request.GET.get(
        'search', False) == "" else request.GET.get('search', False)

    if (search == False and author == False) or (search == "" and author == ""):
        return redirect('/')

    queries = {'q': search, 'inauthor': author, 'key': key}
    print(queries)
    r = requests.get(
        'https://www.googleapis.com/books/v1/volumes', params=queries)
    print(r)
    if r.status_code != 200:
        return render(request, 'book_browse/books.html', {'message': 'Sorry, there seems to be some problems'})

    data = r.json()

    if not 'items' in data:
        return render(request, 'book_browse/books.html', {'message': 'No books match that search term.'})

    fetched_books = data['items']
    books = []
    for book in fetched_books:
        book_dict = {
            'title': book['volumeInfo']['title'],
            'image': book['volumeInfo']['imageLinks']['thumbnail'] if 'imageLinks' in book['volumeInfo'] else "https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg",
            'authors': ", ".join(book['volumeInfo']['authors']) if 'authors' in book['volumeInfo'] else "",
            'publisher': book['volumeInfo']['publisher'] if 'publisher' in book['volumeInfo'] else "",
            'info': book['volumeInfo']['infoLink'],
            'popularity': book['volumeInfo']['ratingsCount'] if 'ratingsCount' in book['volumeInfo'] else 0,
            'published': book['volumeInfo']['publishedDate']if "publishedDate" in book['volumeInfo'] else "",
            'pageCount': book['volumeInfo']['pageCount']if 'pageCount' in book['volumeInfo'] else "No info about pages",
        }
        books.append(book_dict)
    for i in books:
        bookers = Books(
            title=i["title"],
            author=i["authors"],
            cover_link=i["image"],
            publication_date=i["published"],
            number_of_pages=i["pageCount"],
        )
        bookers.save()
    def sort_by_pop(e):
        return e['popularity']

    books.sort(reverse=True, key=sort_by_pop)

    return render(request, 'book_browse/books.html', {'books': books})

def storage(request):
    posts = Books.objects.all()
    return render(request, 'book_browse/cart.html', {'posts': posts})


def dbsearch(title):
     Books.objects.filter(Q(title__icontains=title))