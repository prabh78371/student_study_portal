
from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    
    path('',views.home,name='home'),
    path('notes',views.notes,name='notes'),
    path('delete/<int:pk>',views.delete,name='delete'),
    path('notes_detail/<int:pk>',views.NotesdetailView.as_view(),name='notes_detail'),
    path('homework',views.homework,name='homework'),
    path('update_homework/<int:pk>',views.update_homework,name='update_homework'),
    path('delete_homework/<int:pk>',views.delete_homework,name="delete_homework"),
    path('youtube',views.youtube,name="youtube"),
    path('todo',views.Todo,name="todo"),
    path('update_todo/<int:pk>',views.update_todo,name='update-todo'),
    path('delete_todo/<int:pk>',views.delete_todo,name='delete-todo'),
    path('books',views.books,name='books'),
    path('dic',views.dictionary,name='dictionary'),
    path('wiki',views.wiki,name='wiki'),
    path('profile',views.profile,name='profile')
    
]
