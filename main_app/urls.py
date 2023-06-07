from django.urls import path
from . import views

urlpatterns = [
		path('', views.home, name='home'),
        path('about/', views.about, name= 'about' ),
        path('characters/', views.display_char, name='characters'),
        path('search/', views.search_characters, name='search_characters'),
        path('characters/<int:character_id>/', views.character_details, name='details'),
        path('accounts/signup/', views.signup, name='signup'),
] 