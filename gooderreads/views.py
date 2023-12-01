from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

import json
from urllib.request import urlopen

from .models import Book, Saved

def index(request):
    latest_book_list = Book.objects.order_by("title")[:5]
    context = {"latest_book_list":latest_book_list}
    return render(request, "gooderreads/index.html", context)

def search(request, title):
    api = "https://www.googleapis.com/books/v1/volumes?q=isbn:"
    isbn = input("Enter 10 digit ISBN: ").strip()

    # send a request and get a JSON response
    resp = urlopen(api + isbn)
    # parse JSON into Python as a dictionary
    book_data = json.load(resp)

    # create additional variables for easy querying
    volume_info = book_data["items"][0]["volumeInfo"]
    author = volume_info["authors"]
    # practice with conditional expressions!
    prettify_author = author if len(author) > 1 else author[0]

    # display title, author, page count, publication date
    # fstrings require Python 3.6 or higher
    # \n adds a new line for easier reading
    print(f"\nTitle: {volume_info['title']}")
    print(f"Author: {prettify_author}")
    print(f"Page Count: {volume_info['pageCount']}")
    print(f"Publication Date: {volume_info['publishedDate']}")
    print("\n***\n")

def detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    return render(request, "gooderreads/detail.html", {"book": book})    
   
def save(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    new_save = Saved.objects.create_save(book, "11/11/2011", 'Finished', 'Good', 5)
    new_save.save()
    return HttpResponseRedirect(reverse("gooderreads:results", args=(book.id,)))

def results(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    return render(request, "gooderreads/results.html", {"book":book})