from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.views.generic.edit import CreateView,UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.shortcuts import render, redirect
from .models import Character, Team
from marvel import Marvel
from decouple import config
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404
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
    thumbnail_url = path + '.'+ extension
    
    try:
        character = Character.objects.get(character_id=character_data['id'])
    except Character.DoesNotExist:
        character = Character(
            character_id=character_data['id'],
            name=character_data['name'],
            description=character_data['description'] or '',
            thumbnail=thumbnail_url
        )
        character.save()

    return render(request, 'characters/characters_details.html', {
    'char': character,
    'comics': comics
    })

def team_index(request):
    teams = Team.objects.filter(user=request.user)
    return render(request, 'teams/team.html', {'team': teams})

def team_detail(request, team_id):
    team = Team.objects.get(id=team_id)
    characters = team.characters.all()
    id_list=characters.values_list('character_id', flat=True)
    available_characters = Character.objects.exclude(character_id__in=id_list)
    return render(request, 'teams/team_detail.html', {
        'team': team, 
        'characters': characters,
        'available_characters': available_characters
        })

def add_to_team(request, character_id, team_id):
    team = Team.objects.get(id = team_id)
    character = Character.objects.get(id=character_id)
    if character not in team.characters.all():
        team.characters.add(characters)
    return redirect('team', team_id=team_id)

def assoc_char(request, team_id, character_id):
    team = Team.objects.get(id=team_id)
    character = Character.objects.get(character_id=character_id)
    team.characters.add(character)
    return redirect('team_detail', team_id=team_id)

def unassoc_char(request, team_id, character_id):
    team = Team.objects.get(id = team_id)
    character = Character.objects.get(character_id=character_id)
    team.characters.remove(character)
    return redirect('team_detail', team_id=team_id)

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

class TeamCreate(LoginRequiredMixin, CreateView):
    model = Team
    fields = ['name','description']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class TeamUpdate(LoginRequiredMixin, DetailView):
    model = Team
    fields = ['name','description', 'characters']

class TeamDelete(LoginRequiredMixin, DeleteView):
    model = Team
    success_url = '/teams/'