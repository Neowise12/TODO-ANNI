
from pydoc import html
from django.contrib import admin
from django.urls import path

from app.views import home, login, signup , addtodo ,signout,deletetodo,changestatus


urlpatterns = [
    path('', home, name='home'),
    path('signup/', signup, ),
    path('login/', login ,name='login'),
    path('add-todo/', addtodo),
    path('delete-todo/<int:id>', deletetodo),
    path('change-status/<int:id>/<str:status>', changestatus),
    path('logout/', signout),

]
