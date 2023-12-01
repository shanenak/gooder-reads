from django.db import models

class BookManager(models.Manager):
    def create_book(self, title, author):
        book = self.create(title=title, author=author)
        return book

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    
    objects = BookManager()
    
    
class SavedManager(models.Manager):
    def create_save(self, book, saved_date, shelf,  notes, rating):
        save = self.create(book=book, saved_date=saved_date, shelf=shelf, notes=notes, rating=rating)
        return save
    
class Saved(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    saved_date = models.DateTimeField("date published")
    shelf = models.CharField(max_length=200)
    notes = models.CharField(max_length=200)
    rating = models.IntegerField(default=0)
    
    objects=SavedManager()
