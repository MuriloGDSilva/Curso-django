from django.http import HttpResponse
from recipes.views import home, about, ccontacts
from django.urls import path

urlpatterns = [
    path('', home),
    path('contatos/', ccontacts),
    path('sobre/', about)
]
