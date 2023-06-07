from django.shortcuts import render, redirect
from marvel import Marvel
from decouple import config
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .models import Character, Team

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
    response = characters.all()
    marvel_characters = response['data']['results']
    return render(request, 'characters/characters.html', {'characters': marvel_characters})

def search_characters(request):
      query = request.GET.get('query', '')
      response = characters.all(nameStartsWith=query)
      marvel_characters = response['data']['results']
      return render(request, 'characters/characters.html', {'searched_characters': marvel_characters, 'query': query})

def character_details(request, character_id):
    response = characters.get(character_id)
    character = response['data']['results'][0]
    return render(request, 'characters/details.html', {'char': character})


def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('characters')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)