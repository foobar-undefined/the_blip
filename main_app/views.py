from django.shortcuts import render
from marvel import Marvel
from decouple import config
from .models import Characters
import requests
# Create your views here.
marvel = Marvel(
      PUBLIC_KEY=config('PUBLIC_KEY'), 
      PRIVATE_KEY=config('PRIVATE_KEY')
)
characters = marvel.characters

def home(request):
	  return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def display_char(request):
    response = characters.all(name="Black Panther")
    marvel_characters = response['data']['results']
    return render(request, 'characters/characters.html', {'characters': marvel_characters})

def search_characters(request):
      query = request.GET.get('query', '')
      response = characters.all(nameStartsWith=query)
      marvel_characters = response['data']['results']
      return render(request, 'characters/search_char.html', {'characters': marvel_characters, 'query': query})