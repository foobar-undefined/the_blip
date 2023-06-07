from django.db import models
from django.urls import reverse
# Create your models here.

class Characters(models.Model):
    name= models.CharField(max_length=100),
    char_id = models.PositiveIntegerField(primary_key=True)
    image=models.ImageField(upload_to=None, height_field=None, width_field=250, max_length=100),
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={'char_id'})