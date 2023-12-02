from django.urls import path

from . import views

app_name = "gooderreads"
urlpatterns = [
    # ex: /gooderreads/
    path("", views.index, name="index"),
    # ex: /gooderreads/5/
    path("search/<str:search_term>/", views.search, name="search"),
    path("<int:book_id>/", views.detail, name="detail"),
    # ex: /gooderreads/5/vote/
    path("<int:book_id>/save/", views.save, name="save"),
]
