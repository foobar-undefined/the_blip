from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
# Create your models here.

class Character(models.Model):
    name= models.CharField(max_length=100),
    char_id = models.PositiveIntegerField(primary_key=True)
    image=models.ImageField(upload_to='characters', height_field=None, width_field=250, max_length=100),
    user = models.ForeignKey(User, on_delete=models.CASCADE)
 
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={'char_id'})

class Team(models.Model):
    name = models.CharField(max_length=50)
    characters = models.ManyToManyField(Character)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('team_detail', kwargs={'pk': self.pk})