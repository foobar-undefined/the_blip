from django.urls import path
from . import views

urlpatterns = [
		path('', views.home, name='home'),
        path('about/', views.about, name= 'about' ),
        path('characters/', views.display_char, name='characters'),
        path('search/', views.search_characters, name='search_characters'),
        path('characters/<int:character_id>/', views.character_details, name='details'),
        path('add_to_teams/<int:character_id>/<int:team_id>/', views.add_to_team, name='add_to_team'),
        path('teams/team', views.team_index, name='team'),
        path('teams/<int:team_id>/', views.team_detail, name='team_detail'),
        path('teams/<int:team_id>/unassoc_char/<int:character_id>', views.unassoc_char, name='unassoc_char'),
        path('accounts/signup/', views.signup, name='signup'),

]   