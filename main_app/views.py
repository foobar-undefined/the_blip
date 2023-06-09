from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect
from marvel import Marvel
from decouple import config
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404
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
      if query.isnumeric():
        response = characters.get(int(query))
      else:
        response = characters.all(nameStartsWith=query)
      marvel_characters = response['data']['results']
      return render(request, 'characters/characters.html', {'searched_characters': marvel_characters, 'query': query})

def character_details(request, character_id):
    response = characters.get(character_id)
    character_data = response['data']['results'][0]
    comics_response = characters.comics(character_id)
    comics = comics_response['data']['results']
    thumbnail = character_data['thumbnail']
    path = list(thumbnail.values())[0]
    extension = list(thumbnail.values())[1]
    print(path)
    print(extension)
    # thumbnail_path = character_data['thumbnail']['path']
    thumbnail_extension = character_data['thumbnail']['extension']
    thumbnail_url = path + '.'+ extension
    user = request.user 
    
    try:
        character = Character.objects.get(character_id=character_data['id'], user=user)
    except Character.DoesNotExist:
        character = Character(
            character_id=character_data['id'],
            name=character_data['name'],
            description=character_data['description'] or '',
            thumbnail=thumbnail_url,
            user=user  # Associate the character with the user
        )
        character.save()

    return render(request, 'characters/details.html', {
    'char': character,
    'comics': comics
    })

def team_index(request):
    team = Team.objects.all()
    return render(request, 'teams/team.html', {'team': team})

def team_detail(request, team_id):
    team = Team.objects.get(id=team_id)
    return render(request, 'teams/team_detail.html', {'team': team})

def add_to_team(request, char_id):
    team_character = get_object_or_404(Character, char_id = char_id)
    user = request.user
    team = user.team
    if team_character not in team.characters.all():
        team.characters.add(characters)

    return redirect('team', team_id=team.id)


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