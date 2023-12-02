from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

import requests 
import os
from dotenv import load_dotenv
from datetime import date

from .models import Book, Saved

def index(request):
    latest_book_list = list(set(Book.objects.order_by("title")))
    context = {"latest_book_list":latest_book_list}
    return render(request, "gooderreads/index.html", context)

def search(request, search_term):
    load_dotenv()
    GOOGLE_KEY = os.environ.get('GOOGLE_API_KEY')
    parms = {"q": search_term, 'key': GOOGLE_KEY}
    r = requests.get(url="https://www.googleapis.com/books/v1/volumes", params=parms)
    rj = r.json()
    for i in rj["items"][:10]:
        res_title = i['volumeInfo']['title']
        res_authors = i['volumeInfo']['authors'] if 'authors' in i['volumeInfo'] else 'No author'
        if not Book.objects.filter(title__iexact=res_title).exists():
            print(res_title)
            new_book = Book.objects.create_book(
                res_title, " ".join(res_authors))
            new_book.save()
    latest_book_list = list(set(Book.objects.filter(
        title__contains=search_term).order_by("title")))
    context = {"latest_book_list": latest_book_list}
    return render(request, "gooderreads/index.html", context)


def detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    return render(request, "gooderreads/detail.html", {"book": book})    
   
def save(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    new_save = Saved.objects.create_save(book, date.today(), 'Finished', 'Good', 5)
    new_save.save()
    return HttpResponseRedirect(reverse("gooderreads:results", args=(book.id,)))

def results(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    return render(request, "gooderreads/results.html", {"book":book})