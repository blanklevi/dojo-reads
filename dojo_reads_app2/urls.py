from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('registration', views.registration),
    path('loggedin', views.log_in),
    path('books', views.success_log_in),
    path('logout', views.log_out),
    path('addbook', views.add_book_page),
    path('add_book', views.add_book),
    path('books/<int:book_id>', views.book_page),
    path('delete/<int:review_id>', views.delete_review),
    path('addreview', views.add_review),
    path('users/<int:user_id>', views.user_page),
]
