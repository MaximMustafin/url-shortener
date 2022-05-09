from django.db import models

# Create your models here.


class ShortURL(models.Model):
    """
    A class to represent a model of short url.

    Attributes
    ----------
    hashed_url : str,
        hash-salted full original link
    full_url : str,
        full original link
    number_of_uses : unsigned int,
        number of uses of the short link by the user

    """
    hashed_url = models.CharField(max_length=8, unique=True)
    full_url = models.URLField(unique=True)
    number_of_uses = models.PositiveIntegerField()

