import uuid

from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=100, default='')
    uuid = models.CharField(primary_key=True, max_length=100)
    description = models.CharField(max_length=1000, default='')
    genres = models.CharField(max_length=100, default='')

    def __str__(self) -> str:
        return str(self.title)


class Collection(models.Model):
    title = models.CharField(max_length=100, default='')
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.CharField(max_length=1000, default='')
    movies = models.ManyToManyField(Movie, related_name='collections')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='collections')

    def __str__(self) -> str:
        return str(self.title)
